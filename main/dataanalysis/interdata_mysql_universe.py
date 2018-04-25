import mysql.connector
import re
import random



userid=14

#-------------------------------------------
# Connect to MYSQL and pick out the data
#-------------------------------------------
def getallinterID(hostname):
    db=mysql.connector.connect(host=hostname,
                           database='lccgame',
                           user='host',
                           password='host')
    cursor=db.cursor()
    cursor.execute("SELECT COMM_ID FROM backup_scalsc_states ")
    db.close()
    queryresult=cursor.fetchall()
    newresult=tuple(set(queryresult))
    allinterID=( )
    for i in range(len(newresult)):
        allinterID=allinterID+(newresult[i][0],)
    return allinterID


#get an agent's filled LCC protocol(s) under an interaction ID
def getintagentstates(interactionID):
    db=mysql.connector.connect(host="localhost",
                           database='lccgame',
                           user='host',
                           password='host')
    #db=MySQLdb.connect("localhost","host","host","lccgame")
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

interIDlist=getallinterID('localhost')
print (interIDlist[0])
agent_states=getintagentstates(interIDlist[0])

def getagentinfo(agentinfoclause):
    pattern_agentinfo=re.compile(r'a\(\s*(?P<agentrolename>\w*)\((?P<agentrolevars>.*)\),(?P<agentid>.*)\)::=\\n')
    agent_role_name=re.search(pattern_agentinfo,agentinfoclause).group('agentrolename')
    agent_role_vars=re.search(pattern_agentinfo,agentinfoclause).group('agentrolevars').split(",")
    agent_id=re.search(pattern_agentinfo,agentinfoclause).group('agentid')
    return (agent_role_name,agent_role_vars,agent_id)

    #get message name and var
def getmessageinfo(mbody):
    pattern_msgdir=re.compile(r'(=>|<=)')
    search_msgdir=re.findall(pattern_msgdir,mbody)
    if search_msgdir:
        if(search_msgdir[0]=="=>"):
            pattern_msginfo=re.compile(r'.*c\(\s*(?P<mname>\w*)\((?P<mvars>.*)\)\s=>\s*a\((.*)\).*')
            mvars=re.search(pattern_msginfo,mbody).group('mvars').split(",")
            mname=re.search(pattern_msginfo,mbody).group('mname')
            mdir="out"
            pattern_mtarget=re.compile(r'.*c\(\s*(?P<mname>\w*)\((?P<mvars>.*)\)\s=>\s*a\(\s*(?P<mtarget>\w*)\(.*\),.*?\).*')
            mtarget=re.search(pattern_mtarget,mbody).group('mtarget')
            return (mname,mvars,mdir,mtarget)
        else:
            pattern_msginfo=re.compile(r'.*c\(\s*(?P<mname>\w*)\((?P<mvars>.*)\)\s<=.*')
            mvars=re.search(pattern_msginfo,mbody).group('mvars').split(",")
            mname=re.search(pattern_msginfo,mbody).group('mname')
            mdir="in"
            pattern_mtarget=re.compile(r'.*c\(\s*(?P<mname>\w*)\((?P<mvars>.*)\)\s<=\s*a\(\s*(?P<mtarget>\w*)\(.*\),.*?\).*')
            mtarget=re.search(pattern_mtarget,mbody).group('mtarget')
            return (mname,mvars,mdir,mtarget)
    else:
        return False

