import MySQLdb
import re
import json
from sre_parse import Pattern
from mercurial.statprof import start

def getintset(localhost):
    db=MySQLdb.connect(localhost,"host","host","lccgame")
    cursor=db.cursor()
    cursor.execute("SELECT COMM_ID FROM backup_scalsc_states ")
    db.close()
    queryresult=cursor.fetchall()
    newresult=tuple(set(queryresult))
    intnameset=( )
    for i in range(len(newresult)):
        intnameset=intnameset+(newresult[i][0],)
    return intnameset

def getintagentstates(interactionID): #connect DB and get all agents' states based on interaction  
    db=MySQLdb.connect("localhost","host","host","lccgame")
    cursor=db.cursor()
    cursor.execute("SELECT STATE FROM backup_scalsc_states WHERE COMM_ID=%r" %interactionID)
    agentstates=cursor.fetchall()
    cursor.execute("SELECT PROTOCOL FROM backup_scalsc_states WHERE COMM_ID=%r" %interactionID)
    protocolname=cursor.fetchall()
    db.close()
    agentdef=(agentstates,protocolname[0][0])
    return agentdef
    
#find out how many lines in one agent state
def getclauseset(agentstate):    
    pattern_n=re.compile(r'.*?\\n')
    search_n=re.findall(pattern_n,agentstate)
    return search_n
    
    #get agent role and ID from #2 line 
def getagentinfo(agentinfoclause):
    pattern_agentinfo=re.compile(r'a\(\s*(?P<agentrolename>\w*)\((?P<agentrolevars>.*)\),(?P<agentid>.*)\)::=\\n')
    agent_role_name=re.search(pattern_agentinfo,agentinfoclause).group('agentrolename')
    agent_role_vars=re.search(pattern_agentinfo,agentinfoclause).group('agentrolevars').split(",")
    agent_id=re.search(pattern_agentinfo,agentinfoclause).group('agentid')
    return (agent_role_name,agent_role_vars,agent_id)
    
    #get message name and var 
def getmessageinfo(mbody): 
    pattern_dir=re.compile(r'(=>|<=)')
    search_dir=re.findall(pattern_dir,mbody)
    if search_dir:
        if(search_dir[0]=="=>"):
            pattern_minfo=re.compile(r'.*c\(\s*(?P<mname>\w*)\((?P<mvars>.*)\)\s=>\s*a\((.*)\).*')
            mvars=re.search(pattern_minfo,mbody).group('mvars').split(",")
            mname=re.search(pattern_minfo,mbody).group('mname')
            mdir="out"
            pattern_mtarget=re.compile(r'.*c\(\s*(?P<mname>\w*)\((?P<mvars>.*)\)\s=>\s*a\(\s*(?P<mtarget>\w*)\(.*\),.*?\).*')
            mtarget=re.search(pattern_mtarget,mbody).group('mtarget')
            return (mname,mvars,mdir,mtarget)
        else:
            pattern_minfo=re.compile(r'.*c\(\s*(?P<mname>\w*)\((?P<mvars>.*)\)\s<=.*')
            mvars=re.search(pattern_minfo,mbody).group('mvars').split(",")
            mname=re.search(pattern_minfo,mbody).group('mname')
            mdir="in"
            pattern_mtarget=re.compile(r'.*c\(\s*(?P<mname>\w*)\((?P<mvars>.*)\)\s<=\s*a\(\s*(?P<mtarget>\w*)\(.*\),.*?\).*')
            mtarget=re.search(pattern_mtarget,mbody).group('mtarget')
            return (mname,mvars,mdir,mtarget)
    else:
        return False        


#get all happened interactions
intset=getintset("localhost")
#get agents' states in per interaction

intnum=0
agentstatetree=[ ]
behaviorsequenceinfo=[]
new_behaviorsequenceinfo=[]
while intnum<len(intset):
    intid=intset[intnum]
    intagentstates=getintagentstates(intid)[0]
    intprotocolid=getintagentstates(intid)[1]
    startpoint=len(behaviorsequenceinfo)
    for i in range(len(intagentstates)):
        behaviorsequenceinfo=behaviorsequenceinfo+[{'intid':intid,'protocolid':intprotocolid},]      
    for i in range(len(intagentstates)):
        clauseset=getclauseset(str(intagentstates[i]))
        agent_info=getagentinfo(clauseset[1]) 
        behaviorsequenceinfo[startpoint+i]['role']={'rname':agent_info[0],'rvars':agent_info[1]}
        behaviorsequenceinfo[startpoint+i]['messages']=[]
        linepoint=2
        while linepoint<len(clauseset) and getmessageinfo(clauseset[linepoint]):
            minfo=getmessageinfo(clauseset[linepoint])
            behaviorsequenceinfo[startpoint+i]['messages']=behaviorsequenceinfo[startpoint+i]['messages']+[{'mname':minfo[0],'mvars':minfo[1],'mdir':minfo[2],'mtarget':minfo[3]}]
            linepoint+=1
    intnum+=1
######################################################################3
a=0
while a<len(behaviorsequenceinfo):
    if behaviorsequenceinfo[a]['protocolid']=="ultimategame" and behaviorsequenceinfo[a]['role']['rname']=='responder':
        print behaviorsequenceinfo[a]['messages']
    a+=1
 



