import MySQLdb
import re
import json
from sre_parse import Pattern

def getstate(interactionname):   
    db=MySQLdb.connect("localhost","host","host","lccgame")
    cursor=db.cursor()
    cursor.execute("SELECT STATE FROM backup_scalsc_states WHERE COMM_ID='{}'".format(interactionname))
    b=cursor.fetchall()
    db.close()
    return b

statestupe=getstate("int8282")
for i in statestupe:
    playerstate=str(i)
    
    

playerstate=str(statestupe[1])


#match information
pattern_wholestate=re.compile(r'(\(\'\\n)(?P<State>.*\\n)')
pattern_playerinfo=re.compile(r'(\(\'\\n).*a\(\s*(?P<PlayerRole>.*),(?P<PlayerID>.*)\)::=\\n(.*)')
pattern_1clause=re.compile(r'(\(\'\\n).*::=\\n.*c\(.*(?P<FirstClause>offer.*?\\n)\s*then\\n(.*)')
pattern_2clause=re.compile(r'(\(\'\\n).*::=\\n.*c\(.*(?P<SecondClause>.repay.*?\\n)\s*then\\n(.*)')
pattern_3clause=re.compile(r'(\(\'\\n).*::=\\n.*(?P<ThirdClause>k.*?\\n)\s+(.*)')
trustgame_investor_states=re.search(pattern_wholestate, playerstate).group('State')
trustgame_investor_role=re.search(pattern_playerinfo, playerstate).group('PlayerRole')
trustgame_investor_id=re.search(pattern_playerinfo, playerstate).group('PlayerID')
trustgame_investor_1clause=re.search(pattern_1clause, playerstate).group('FirstClause')
trustgame_investor_2clause=re.search(pattern_2clause, playerstate).group('SecondClause')
trustgame_investor_3clause=re.search(pattern_3clause, playerstate).group('ThirdClause')

pattern_m1_info=re.compile(r'(\(\'\\n).*::=\\n.*c\(\s*offer\((?P<mVar1>.*)\)\s=>(.*?)\\n\s*then\\n(.*)')
pattern_m2_info=re.compile(r'(\(\'\\n).*::=\\n.*c\(\s*repay\((?P<mVar1>.*)\)\s<=(.*)\s*then\\n(.*)')
trustgame_investor_m1_mvar1=re.search(pattern_m1_info,playerstate).group('mVar1')
trustgame_investor_m2_mvar1=re.search(pattern_m2_info,playerstate).group('mVar1')

if trustgame_investor_states:
    print "playerstate is "+playerstate
    print "playerrole is "+trustgame_investor_role
    print "playerid is "+trustgame_investor_id
    print "firstclause is "+trustgame_investor_1clause
    print "secondclause is "+trustgame_investor_2clause
    print "thirdclause is "+trustgame_investor_3clause

    print "Unit m1 is "+trustgame_investor_m1_mvar1
    print "Unit m2 is "+trustgame_investor_m2_mvar1
else:
    print "\nNothing"

print "======================================="

pattern_n=re.compile(r'.*?\\n')
pattern_arrow=re.compile(r'(=>|<=)')
pattern_then=re.compile(r'c\(.*then\\n')
search_n=re.findall(pattern_n,playerstate)
search_arrow=re.findall(pattern_arrow,search_n[2])
search_then=re.findall(pattern_then,playerstate)
print "search_n is "+search_n[2]
print type(search_arrow[0])
print search_then

def getagentinfo(infoclause):
    pattern_agentinfo=re.compile(r'a\(\s(?P<agentrole>.*),(?P<agentid>.*)\)::=\\n')
    agent_role=re.search(pattern_agentinfo,search_n[1]).group('agentrole')
    agent_id=re.search(pattern_agentinfo,search_n[1]).group('agentid')
    return (agent_role,agent_id)
totalnum_n=len(search_n)


def getmvar(mbody,mname): 
    pattern_dir=re.compile(r'(=>|<=)')
    search_dir=re.findall(pattern_dir,mbody)
    if search_dir:
        if(search_dir[0]=="=>"):
            pattern_minfo=re.compile(r'.*c\(\s*(?P<mname>\w*)\((?P<mvar1>.*)\)\s=>(.*)')
            mvar1=re.search(pattern_minfo,mbody).group('mvar1')
            return mvar1
        else:
            pattern_minfo=re.compile(r'.*{}\((?P<mvar1>.*)\)\s<=(.*)'.format(mname))
            mvar1=re.search(pattern_minfo,mbody).group('mvar1')
            return mvar1
    else:
        print "not found arrow"
    
    
print getmvar(search_n[2],"repay")


print "++++++++++++++++++++++++++++++++++++++"
