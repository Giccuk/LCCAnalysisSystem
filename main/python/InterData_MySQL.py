import MySQLdb
import re
import random

#============================================================================
# Connect to MYSQL and pick out the data
#============================================================================
def getallinterID(localhost):
    db=MySQLdb.connect(localhost,"host","host","lccgame")
    cursor=db.cursor()
    cursor.execute("SELECT COMM_ID FROM backup_scalsc_states ")
    db.close()
    queryresult=cursor.fetchall()
    newresult=tuple(set(queryresult))
    allinterID=( )
    for i in range(len(newresult)):
        allinterID=allinterID+(newresult[i][0],)
    return allinterID

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

#interaction_behaviors=[
# {intid,protocolid,role:{rname,rvars},messages:{mname,mvars,mdir,mtarget}},
# {intid,protocolid,role:{rname,rvars},messages:{mname,mvars,mdir,mtarget}},
# ...
# {intid,protocolid,role:{rname,rvars},messages:{mname,mvars,mdir,mtarget}}
# ]
def getgamedataMySQL(dbaddress):
    #get all happened interactions
    interIDset=getallinterID(dbaddress)
    #get agents' states in per interaction
    internum=0
    interaction_behaviors=[]
    for internum in range(len(interIDset)):
        interID=interIDset[internum]
        interagentstates=getintagentstates(interID)[0]
        interprotocolID=getintagentstates(interID)[1]
        startpoint=len(interaction_behaviors)
        for i in range(len(interagentstates)):
            interaction_behaviors=interaction_behaviors+[{'intid':interID,'protocolid':interprotocolID},]
        for i in range(len(interagentstates)):
            clauseset=getclauseset(str(interagentstates[i]))
            agent_info=getagentinfo(clauseset[1])
            interaction_behaviors[startpoint+i]['role']={'rname':agent_info[0],'rvars':agent_info[1]}
            interaction_behaviors[startpoint+i]['messages']=[]
            for linepoint in range(2,len(clauseset)):
                if getmessageinfo(clauseset[linepoint]):
                    minfo=getmessageinfo(clauseset[linepoint])
                    interaction_behaviors[startpoint+i]['messages']=interaction_behaviors[startpoint+i]['messages']+[{'mname':minfo[0],'mvars':minfo[1],'mdir':minfo[2],'mtarget':minfo[3]},]
    return interaction_behaviors

#==================================================
#Query for information from interacion sequences
#==================================================

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
# Get Interaction Patterns
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

