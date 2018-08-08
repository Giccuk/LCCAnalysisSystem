import mysql.connector
import re
import random
from collections import deque
import copy

#================================================================================
# Connect to MYSQL and pick out the data
#================================================================================
#--------------------------------------------------------------------------------------
# fun: get all the interaction ID in a table eg. gamemsgs2, playerinfo2, backup_scalsc_states
# input: tablename
# outout:['int1244','int222',...,'int2323']
#--------------------------------------------------------------------------------------
def getallinterid(tablename):
    db=mysql.connector.connect(host="localhost",
                           database='lccgame',
                           user='host',
                           password='host')
    cursor=db.cursor()
    #cursor.execute("SELECT COMM_ID FROM backup_scalsc_states ")
    if tablename=='backup_scalsc_states':
        querycomd="SELECT COMM_ID FROM %s"%tablename
    else:
        querycomd="SELECT interid FROM %s"%tablename
    cursor.execute(querycomd)
    db.close()
    queryresult=cursor.fetchall()
    newresult=list(set(queryresult))#delete dupilcate elements
    allinterID=[]
    for i in range(len(newresult)):
        allinterID=allinterID+[newresult[i][0]]
    return allinterID

#--------------------------------------------------------------------------------------
# fun: get all the agent ID in backup_scalsc_states
# input: none
# outout:['p12','p14',...]
#--------------------------------------------------------------------------------------
def getallagentid():
    db=mysql.connector.connect(host="localhost",
                           database='lccgame',
                           user='host',
                           password='host')
    cursor=db.cursor()
    #cursor.execute("SELECT COMM_ID FROM backup_scalsc_states ")
    querycomd="SELECT agent_id FROM backup_scalsc_states"
    cursor.execute(querycomd)
    db.close()
    queryresult=cursor.fetchall()
    newresult=list(set(queryresult))#delete dupilcate elements
    allagentID=[]
    for i in range(len(newresult)):
        allagentID=allagentID+[newresult[i][0]]
    return allagentID


#---------------------------------------------------------------------------------------
# fun: Get an agent's filled LCC protocol(s) under a interaction ID in backup_scalsc_states
# input: int123
# output: {'agentid','protocol','agentrole','interid','interdata'}
# eg. interdata_byinterid=[['interid','protocolname',['a()::=','c(x()=>a())','then',....],'agentrole','agentid'],
#                      ['interid','protocolname',['a()::=','c(x()<=a())','then',....],'agentrole','agentid'],
#                      ...
#                      ['interid','protocolname',['a()::=','c(z()=>a())','then',....],'agentrole','agentid'],
#                     ]
#--------------------------------------------------------------------------------------
def getinterdata_byinterid(interaction_id):
    db=mysql.connector.connect(host="localhost",
                               database='lccgame',
                               user='host',
                               password='host')
    cursor=db.cursor()
    cursor.execute("SELECT AGENT_ID,ROLE,PROTOCOL,COMM_ID,STATE FROM backup_scalsc_states WHERE COMM_ID=%r" %interaction_id)
    interdata=cursor.fetchall()
    cursor.close()
    db.close()

    interdata_list=[]
    for i in range(len(interdata)):
        interdata_split=re.split(r'\n\s+',interdata[i][4])
        interdata_split_noempty=[x for x in interdata_split if x!='']
        interdata_list.append({
            'agentid':interdata[i][0],
            'agentrole':interdata[i][1],
            'protocol':interdata[i][2],
            'interid':interaction_id,
            'states':interdata_split_noempty
        })
    return interdata_list

#-----------------------------------------------------------------------------------------------------------------
# fun: Get an agent's filled LCC protocol(s) under an agent ID in backup_scalsc_states
# input: p12
# output: {'agentid','protocol','agentrole','interid','interdata'}
# eg. interdata_byinterid=[['interid','protocolname',['a()::=','c(x()=>a())','then',....],'agentrole','agentid'],
#                      ['interid','protocolname',['a()::=','c(x()<=a())','then',....],'agentrole','agentid'],
#                      ...
#                      ['interid','protocolname',['a()::=','c(z()=>a())','then',....],'agentrole','agentid'],
#                     ]
#-----------------------------------------------------------------------------------------------------------------
def getinterdata_byagentid(agent_id):
    db=mysql.connector.connect(host="localhost",
                               database='lccgame',
                               user='host',
                               password='host')
    cursor=db.cursor()
    cursor.execute("SELECT PROTOCOL,ROLE,COMM_ID,STATE FROM backup_scalsc_states WHERE AGENT_ID=%r" %agent_id)
    interdata=cursor.fetchall()
    cursor.close()
    db.close()
    interdata_list=[]
    for i in range(len(interdata)):
        interdata_split=re.split(r'\n\s+',interdata[i][3])
        interdata_split_noempty=[x for x in interdata_split if x!='']
        interdata_list.append({
            'agentid':agent_id,
            'protocol':interdata[i][0],
            'agentrole':interdata[i][1],
            'interid':interdata[i][2],
            'states':interdata_split_noempty
        })
    return interdata_list

#===================================================================================================================================================================
#Process the protocol
#===================================================================================================================================================================
# -----------------------------------------------------
# fun: Get an agent's definition information
# input: \na()::=
# output: a()
# -----------------------------------------------------
def parseroledef(roledefclause):
    p_roledef = re.compile(r'\n(a\(.*\))\s*::=')
    m_roledef = re.match(p_roledef, roledefclause)
    if m_roledef:
        return m_roledef.group(1)
    else:
        return False


# -----------------------------------------------------
# fun: Get an agent's definition information
# input: a()
# output: {'agentinfo_rolename':agentinfo_rolename,'agentinfo_rolevars:':agentinfo_rolevars,'agentinfo_id':agentinfo_id}
# -----------------------------------------------------
def getroledef_detail(roledef):
    agentinfo_pattern = re.compile(r'\s*a\(\s*(?P<agentrolename>\w*)\((?P<agentrolevars>.*)\),(?P<agentid>.*)\)')
    agentinfo_match = agentinfo_pattern.match(roledef)
    if agentinfo_match:
        agentinfo_rolename = agentinfo_match.group('agentrolename')
        agentinfo_rolevars = agentinfo_match.group('agentrolevars')
        agentinfo_id = agentinfo_match.group('agentid')
        agentinfo = {'rolename': agentinfo_rolename, 'rolevars': agentinfo_rolevars, 'roleid': agentinfo_id}
        return agentinfo
    else:
        return False


# -----------------------------------------------------
# fun: parse closed inter action to dictionary
# input: c(m()<=a()), c(m()=>a())
# output: {'intermessage':m(),'interact':'send'|'get','interpartner':a()}
# -----------------------------------------------------
def parseinteraction(interaction):
    p_doublearrow = re.compile(r'(<=|=>)')
    p_mbody = re.compile(r'\s*c\(\s*(\w+\(.*\))')
    p_mtarget = re.compile(r'\s*(a\(\s*.*\)):.*')
    m_doublearrow = re.search(p_doublearrow, interaction)
    if m_doublearrow:
        m_split = re.split(p_doublearrow, interaction)
        mbody = re.match(p_mbody, m_split[0]).group(1)
        mtarget = re.match(p_mtarget, m_split[2]).group(1)
        if m_doublearrow.group() == "<=":
            mdir = 'get'
        else:
            mdir = 'send'
        return {'messagebody': mbody, 'messagedirection': mdir, 'messagepartner': mtarget}
    else:
        return False


# ------------------------------------------
# fun: Get message details
# input: m(x)
# output:{'mname':...,'mvars':...}
# ------------------------------------------
def getmessage_detail(messagedata):
    p_message = re.compile(r'\s*(?P<mname>\w*)\((?P<mvars>.*)\s*\)')
    m_message = re.match(p_message, messagedata)
    return {'messagename': m_message.group('mname'), 'messagecontent': m_message.group('mvars')}


# ------------------------------------------------------
# fun: parse closed solo action to the cersion without
# input: c(k()),c(i()),c(e())
# output: k()|i()|e()
# ------------------------------------------------------
def parsesoloaction(soloactionclause):
    p_soloaction = re.compile(r'\s*c\(\s*(?P<actionbody>\w*\(.*\))\s*:.*\)\s*')
    m_soloaction = re.match(p_soloaction, soloactionclause)
    return m_soloaction.group(1)


# ------------------------------------------------------
# fun: get details from solo action
# input: k(),i(),e()
# output: {'solocationname':'e,'solocationvars':'acceptornot(reject,c)'}
# ------------------------------------------------------
def getsoloaction_detail(soloaction):
    p_soloaction_detail = re.compile(r'\s*(?P<saname>\w*)\((?P<savars>.*)\)')
    m_soloaction_detail = re.match(p_soloaction_detail, soloaction)
    return {'soloactionname': m_soloaction_detail.group('saname'),
            'soloactioncontent': m_soloaction_detail.group('savars')}


# --------------------------------------------
# fun: parse closed element into different dictionary
# input: c()
# output: {'elementtype':'interaction',"elementcontent":interact|soloact}
# --------------------------------------------
def parseclosedelement(closedelement):
    p_doublearrow = re.compile(r'(<=|=>)')
    m_doublearrow = re.search(p_doublearrow, closedelement)
    if m_doublearrow:  # inter act element
        return {'closedactiontype': 'interaction', "closedactioncontent": parseinteraction(closedelement)}
    else:
        return {'closedactiontype': 'soloaction', "closedactioncontent": parsesoloaction(closedelement)}

#-----------------------------------------------------
# fun: parse one generic clause to different structure
# input: c()<--c(), c(), \na()::=, then
# output: send clause(sendaction, *constraint),
#         get clause(getaction, *next action),
#         computing clauses(resultaction, preaction)
#         connector,
#         agent definition
#-----------------------------------------------------
def parsegenericclause(inputclause):
    p_singlearrow=re.compile(r'<-+')
    p_doublearrow=re.compile(r'(<=|=>)')
    p_closesign=re.compile(r'c\(')
    p_close=re.compile(r'\s*c\(\s*(\w*\(.*\)):.*\)')
    m_closesign=re.match(p_closesign,inputclause)
    if m_closesign:# c(...) or c(...)<--c(...)
        m_elementlist=re.split(p_singlearrow,inputclause)# 使用’<--’来分割 clause
        if len(m_elementlist)==1:# c(...)
            result=parseclosedelement(inputclause)
            return{'clausetype':result['closedactiontype'],'clausecontent':result['closedactioncontent']}
        else:# c(...) <- c(...)
            resultaction=parseclosedelement(m_elementlist[0])
            causeaction=parseclosedelement(m_elementlist[1])
            return{'clausetype':'multipleaction','clausecontent':{'resultactiontype':resultaction['closedactiontype'],\
                                                                  'resultactioncontent':resultaction['closedactioncontent'],\
                                                                  'causeactiontype':causeaction['closedactiontype'],\
                                                                  'causeactioncontent':causeaction['closedactioncontent']
                                                                 }}
    else:# no c(...)
        if parseroledef(inputclause):
            #print("Agent Definition:",parseroledef(subject))
            return{'clausetype':'roledefinition','clausecontent':parseroledef(inputclause)}
        else:
            #print("Connector:",subject)
            return{'clausetype':'connector','clausecontent':inputclause}

#-----------------------------------------------------------------------------------------------------
# fun: transform an old interdata into a new interdata in which 'states' is 'deque' type
# input: old_interdata=[{'agentid','protocol','agentrole','interid','states':['...','...','...','...']]
# output: new_interdata=[{'agentid','protocol','agentrole','interid',
#                         'states':deque([
#                                          {'clausetype':...,'clauescontent':...},
#                                          {'clausetype':...,'clauescontent':...},
#                                          {'clausetype':...,'clauescontent':...}
#                                       ])
#-----------------------------------------------------------------------------------------------------
def getnewinterdata_dll(old_interdata):
    new_interdata=copy.deepcopy(old_interdata)
    for i in range(len(new_interdata)):
        agentrole=getroledef_detail(new_interdata[i]['agentrole'])
        state=new_interdata[i]['states']
        stateslist=deque()
        for j in range(len(state)):
            if j!=0:
                parsedclause=parsegenericclause(state[j])
                if parsedclause['clausetype']!='connector':
                    stateslist.append(parsedclause)
        new_interdata[i]['agentrole']=agentrole
        new_interdata[i]['states']=stateslist
    return new_interdata

'''
#get all agents' ids
agentidlist=getallagentid()
#get p12's interdata
interdata_p12=getnewinterdata_dll(getinterdata_byagentid('p12'))
#--------------------------------------------------------
# get p12: responder's choice and the offer number
#--------------------------------------------------------

#get p12's reject data and accept data
search_subject={'rolename':'responder','protocol':'ultimategame'}
rejectlist=[]
acceptlist=[]
for i in range(len(interdata_p12)):
    if interdata_p12[i]['agentrole']['rolename']==search_subject['rolename']\
    and interdata_p12[i]['protocol']==search_subject['protocol']:
        states=interdata_p12[i]['states']
        for j in range(len(states)):
            if states[j]['clausetype']=='multipleaction':
                ebody=states[j]['clausecontent']['causeactioncontent']
                ebody_content=getsoloaction_detail(ebody)
                ebody_content_detail=getmessage_detail(ebody_content['soloactioncontent'])
                p_choice=re.compile(r'(?P<choice>\w*),\s*(?P<offer>\d*\.*\d*)')
                m_choice=re.search(p_choice,ebody_content_detail['messagecontent'])
                if 'reject'==m_choice.group('choice'):
                    rejectlist.append([m_choice.group('offer'),interdata_p12[i]['agentrole']['rolevars'],interdata_p12[i]['interid']])
                else:
                    acceptlist.append([m_choice.group('offer'),interdata_p12[i]['agentrole']['rolevars'],interdata_p12[i]['interid']])
                    
rejectratio=[]
acceptratio=[]
for i in range(len(rejectlist)):
    try:
        rejectratio.append([float(rejectlist[i][0])/float(rejectlist[i][1]),rejectlist[i][2]])
    except:
        print("the %dth can't be flaoted"%i)
for j in range(len(acceptlist)):
    try:
        acceptratio.append([float(acceptlist[j][0])/float(acceptlist[j][1]),acceptlist[j][2]])
    except:
        print("the %dth can't be flaoted"%j)
    
print(rejectratio)
print(acceptratio)

#--------------------------------------------------------
# get p12: trustee's repay and received offer
#--------------------------------------------------------
#get p12's reject data and accept data
search_subject2={'rolename':'trustee','protocol':'trustgame_simple'}
repaynum_list=[]
for i in range(len(interdata_p12)):
    if interdata_p12[i]['agentrole']['rolename']==search_subject2['rolename']\
        and interdata_p12[i]['protocol']==search_subject2['protocol']:
        states=interdata_p12[i]['states']
        for j in range(len(states)):
            if states[j]['clausetype']=='multipleaction':
                causeaction_content=states[j]['clausecontent']['causeactioncontent']
                causeaction_content_detail=getsoloaction_detail(causeaction_content)
                if causeaction_content_detail['soloactionname']=='e':
                    repay_action=getmessage_detail(causeaction_content_detail['soloactioncontent'])
                    if "repay" in repay_action['messagename']:
                        p_repay=re.compile(r'\d*\.*\d*')
                        m_repay=p_repay.search(repay_action['messagecontent'])
                        #print("repay num: ",m_repay.group())
                        repay_num=m_repay.group()
                resultaction_type=states[j]['clausecontent']['resultactiontype']
                if resultaction_type=='soloaction':
                    resultaction_content=states[j]['clausecontent']['resultactioncontent']
                    resultaction_content_detail=getsoloaction_detail(resultaction_content)
                    if resultaction_content_detail['soloactionname']=='k' and 'get' in resultaction_content_detail['soloactioncontent']:
                        p_get=re.compile(r'get\((\d*\.*\d*)\)')
                        m_get=p_get.search(resultaction_content_detail['soloactioncontent'])
                        #print("get num: ",m_get.group(1))
                        #print(resultaction_content)
                        get_num=m_get.group(1)
        repaynum_list.append([repay_num,get_num,interdata_p12[i]['interid']])

repayratio_list=[]
error_list=[]
for i in range(len(repaynum_list)):
    try:
        if float(repaynum_list[i][1])!=0:
            repayratio_list.append([float(repaynum_list[i][0])/float(repaynum_list[i][1]),repaynum_list[i][2]]) 
        else:
            repayratio_list.append([0,repaynum_list[i][2]])
    except:
        print("the %dth in repaylist_num can't be floated"%i)
        error_list.append(i)

"""
print(repaynum_list)
print(repayratio_list)
"""

'''


