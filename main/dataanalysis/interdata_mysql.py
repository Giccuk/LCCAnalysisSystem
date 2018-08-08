import mysql.connector
#impirt MySQLdb
import re
import random

#-------------------------------------------
# Connect to MYSQL and pick out the data
#-------------------------------------------
#---------------------------------
#fun: get all interID in lccgame from backup_scalsc_states under a hostname (eg.locakhost)
#in: hostname
#out: interid,eg.['inter11','int12']
#---------------------------------
def getallinterID(hostname):
    db=mysql.connector.connect(host=hostname,
                           database='lccgame',
                           user='host',
                           password='host')
    #db=MySQLdb.connect(localhost,"host","host","lccgame")
    cursor=db.cursor()
    cursor.execute("SELECT COMM_ID FROM backup_scalsc_states ")
    db.close()
    queryresult=cursor.fetchall()
    newresult=tuple(set(queryresult))
    allinterID=( )
    for i in range(len(newresult)):
        allinterID=allinterID+(newresult[i][0],)
    return allinterID
#---------------------------------
#fun: get interdata under an interID from backup_scalsc_states
#in: interID
#---------------------------------
def getinterdata(interactionID): #connect DB and get all agents' states based on interaction
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
#---------------------------------
#fun: find out how many lines in one agent state
#---------------------------------
def getclauseset(agentstate):
    pattern_n=re.compile(r'.*?\\n')
    search_n=re.findall(pattern_n,agentstate)
    return search_n

    #get agent role and ID from #2 line
def getagentdef(agentinfoclause):
    pattern_agentinfo=re.compile(r'a\(\s*(?P<agentrolename>\w*)\((?P<agentrolevars>.*)\),(?P<agentid>.*)\)::=\\n')
    agent_role_name=re.search(pattern_agentinfo,agentinfoclause).group('agentrolename')
    agent_role_vars=re.search(pattern_agentinfo,agentinfoclause).group('agentrolevars').split(",")
    agent_id=re.search(pattern_agentinfo,agentinfoclause).group('agentid')
    return (agent_role_name,agent_role_vars,agent_id)

    #get message name and var
def getagentaction(mbody):
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

# ---------------------------------
#fun: get interdata from backup_scalsc_states
#int: hostname
#out:
#interaction_behaviors=[
# {intid,protocolid,role:{rname,rvars},messages:{mname,mvars,mdir,mtarget}},
# {intid,protocolid,role:{rname,rvars},messages:{mname,mvars,mdir,mtarget}},
# ...
# {intid,protocolid,role:{rname,rvars},messages:{mname,mvars,mdir,mtarget}}
# ]
#---------------------------------
def getgamedataMySQL(dbaddress):
    #get all happened interactions
    interIDset=getallinterID(dbaddress)
    #get agents' states in per interaction
    internum=0
    interaction_behaviors=[]
    for internum in range(len(interIDset)):
        interID=interIDset[internum]
        interagentstates=getinterdata(interID)[0]
        interprotocolID=getinterdata(interID)[1]
        startpoint=len(interaction_behaviors)
        for i in range(len(interagentstates)):
            interaction_behaviors=interaction_behaviors+[{'intid':interID,'protocolid':interprotocolID},]
        for i in range(len(interagentstates)):
            clauseset=getclauseset(str(interagentstates[i]))
            agent_info=getagentdef(clauseset[1])
            interaction_behaviors[startpoint+i]['role']={'rname':agent_info[0],'rvars':agent_info[1]}
            interaction_behaviors[startpoint+i]['messages']=[]
            for linepoint in range(2,len(clauseset)):
                if getagentaction(clauseset[linepoint]):
                    msginfo=getagentaction(clauseset[linepoint])
                    interaction_behaviors[startpoint+i]['messages']=interaction_behaviors[startpoint+i]['messages']+[{'mname':msginfo[0],'mvars':msginfo[1],'mdir':msginfo[2],'mtarget':msginfo[3]},]
    return interaction_behaviors

#==================================================
#Query for information from interacion sequences
#==================================================

# get all proposers' offer ratio
def getofferratio(gamedata):
    offerratio=[]
    for i in range(len(gamedata)):
        if (gamedata[i]['protocolid']=='ultimategame' and gamedata[i]['role']['rname']=='proposer'):
            wholeamount=gamedata[i]['role']['rvars'][0]
            for j in range(len(gamedata[i]['messages'])):
                if gamedata[i]['messages'][j]['mname']=='offer':
                    theratio=float(gamedata[i]['messages'][j]['mvars'][0])/float(wholeamount)
                    offerratio=offerratio+[theratio,]
    return offerratio

# get all responders' acceptornot ratio
def getacceptornotratio(gamedata):
    acceptratio=[]
    rejectratio=[]
    for i in range(len(gamedata)):
        if (gamedata[i]['protocolid']=='ultimategame' and gamedata[i]['role']['rname']=='responder'):
            acceptamount=0
            rejectamount=0
            theratio=0
            totalamount=gamedata[i]['role']['rvars'][0]
            for j in range(len(gamedata[i]['messages'])):
                if gamedata[i]['messages'][j]['mname']=='decide' and gamedata[i]['messages'][j]['mvars'][0]=='accept':
                    acceptamount=gamedata[i]['messages'][j]['mvars'][1]
                elif gamedata[i]['messages'][j]['mname']=='decide' and gamedata[i]['messages'][j]['mvars'][0]=='reject':
                    rejectamount=gamedata[i]['messages'][j]['mvars'][1]
                if acceptamount!=0:
                    theratio=round(float(acceptamount)/float(totalamount),2)
                    acceptratio=acceptratio+[theratio,]
                if rejectamount!=0:
                    theratio=round(float(rejectamount)/float(totalamount),2)
                    rejectratio=rejectratio+[theratio,]
    return [acceptratio,rejectratio]

def getinvestratio(gamedata):
    investratio=[]
    for i in range(len(gamedata)):
        if (gamedata[i]['protocolid']=='trustgame_simple' and gamedata[i]['role']['rname']=='investor'):
            investorown=gamedata[i]['role']['rvars'][0]
            for j in range(len(gamedata[i]['messages'])):
                if gamedata[i]['messages'][j]['mname']=='offer':
                    theratio=float(gamedata[i]['messages'][j]['mvars'][0])/float(investorown)
            investratio=investratio+[theratio,]
    return investratio

def getrepayratio(gamedata):
    repayratio=[]
    for i in range(len(gamedata)):
        if (gamedata[i]['protocolid']=='trustgame_simple' and gamedata[i]['role']['rname']=='trustee'):
            exchangeratio=gamedata[i]['role']['rvars'][0]
            offeramount=0
            for j in range(len(gamedata[i]['messages'])):
                if gamedata[i]['messages'][j]['mname']=='offer':
                    offeramount=gamedata[i]['messages'][j]['mvars'][0]
                if gamedata[i]['messages'][j]['mname']=='repay':
                    repayamount=gamedata[i]['messages'][j]['mvars'][0]
            if offeramount!=0:
                theratio=float(repayamount)/(float(offeramount)*float(exchangeratio))
                repayratio=repayratio+[round(theratio,2),]
    return repayratio


#==============================================
# fun: Get Interaction Patterns
# in: hostname
# out: [[offerratio1,accpetratio1],
#       [offerratio2,accpetratio2],
#       ...
#      ]
#==============================================
def get_interactiondata_MySQL(dbaddress):
	gamemessages=getgamedataMySQL(dbaddress)
	offerratio=getofferratio(gamemessages)
	acceptornotratio=getacceptornotratio(gamemessages)
	investratio=getinvestratio(gamemessages)
	repayratio=getrepayratio(gamemessages)
	interaction_patterns=[]
	#labels=[]
	for i in range(len(offerratio)):
		if i<len(acceptornotratio[0]):
			#print [offerratio[i],acceptornotratio[0][i]]
			interaction_patterns=interaction_patterns+[[offerratio[i],acceptornotratio[0][i]]]
		else:
			j=i-len(acceptornotratio[0])
			#print [offerratio[i],acceptornotratio[1][j]]
			interaction_patterns=interaction_patterns+[[offerratio[i],acceptornotratio[1][j]]]
		#label_rand=random.randint(0,2)
		#labels=labels+[label_rand]
	return samples

