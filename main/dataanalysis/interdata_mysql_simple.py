import mysql.connector
import re
import random

#############################################
# Connect MySQL
#############################################
#==============================================================================================
# name: get_gamemsgs
# in: none
# out: list consisted of game messages
# fun: connect mydql data set "gamemsgs" and "playerinfo" to build interaction data set
#==============================================================================================

def querymysql(query_command):
    db=mysql.connector.connect(host='localhost',
                           database='lccgame',
                           user='host',
                           password='host')
    cursor=db.cursor()
    cursor.execute(query_command)
    db.close()
    queryresult=cursor.fetchall()
    return queryresult

userid=14

def get_proposeroffer(userid):
    proposeroffer=[]
    role='proposer'+'%'
    repattern_gamemsg = re.compile(r'e\((?P<msgname>\w*)\((?P<msgvars>.*)\)\)')
    #get the user's messages as proposer about offer amount
    querycommand_po="""SELECT gamemsgs.msgbody
                        FROM playerinfo
                        INNER JOIN gamemsgs 
                        ON playerinfo.interid=gamemsgs.interid
                        WHERE ( playerinfo.userid=%s
                            AND playerinfo.playerrole LIKE "%s"
                            AND playerinfo.playerrole=gamemsgs.msgsenderrole )
                    """%(userid,role)
    msglist_propser_sender=querymysql(querycommand_po)
    # extract offer values from the messages
    for i in msglist_propser_sender:
        msg_vars=re.search(repattern_gamemsg,i[0]).group('msgvars').split('#')
        proposeroffer=proposeroffer+[int(msg_vars[0])]
    # return the min and max values of the offers
    return proposeroffer

def get_proposeroffer_ratio(userid):
    proposerofferratio=[]
    role='proposer'+'%'
    repattern_gamemsg = re.compile(r'e\((?P<msgname>\w*)\((?P<msgvars>.*)\)\)')
    repattern_userinfo = re.compile(r'(?P<userrolename>\w*)\((?P<agentrolevars>.*)\)')
    #get the user's messages as proposer about offer amount
    querycommand_po="""SELECT gamemsgs.msgbody,playerinfo.playerrole,playerinfo.interid
                        FROM playerinfo
                        INNER JOIN gamemsgs 
                        ON playerinfo.interid=gamemsgs.interid
                        WHERE ( playerinfo.userid=%s 
                            AND playerinfo.playerrole LIKE "%s"
                            AND playerinfo.playerrole=gamemsgs.msgsenderrole )
                        ORDER BY playerinfo.interid
                    """%(userid,role)
    msglist_propser_sender=querymysql(querycommand_po)
    # extract offer values from the messages
    for i in msglist_propser_sender:
        proposer_offer=re.search(repattern_gamemsg,i[0]).group('msgvars').split('#')
        game_total=re.search(repattern_userinfo,i[1]).group('agentrolevars')
        proposerofferratio=proposerofferratio+[int(proposer_offer[0])/int(game_total)]
    # return the min and max values of the offers
    return proposerofferratio



def get_trusteerepay_ratio(userid):
    role='trustee'+'%'
    repattern_gamemsg = re.compile(r'e\((?P<msgname>\w*)\((?P<msgvars>.*)\)\)')
    repattern_userinfo=re.compile(r'(?P<userrolename>\w*)\((?P<agentrolevars>.*)\)')
    trusteeget=[]#[[int:trusteeget,int:interid],...,[]]
    trusteerepay=[]#[[int:trusteerepay,int:interid],...,[]]
    trusteerepayratio=[]#[float:trusteerepayratio]
    #get values that the user gets as trustee
    querycommand_tg="""SELECT gamemsgs.msgbody,playerinfo.playerrole,playerinfo.interid
                            FROM playerinfo
                            INNER JOIN gamemsgs 
                            ON playerinfo.interid=gamemsgs.interid
                            WHERE(playerinfo.userid=%s
                                AND playerinfo.playerrole LIKE "%s"
                                AND playerinfo.playerrole=gamemsgs.msgreceiverrole )
                            ORDER BY playerinfo.interid
                        """%(userid,role)
    msglist_trusteeget=querymysql(querycommand_tg)#[msgbody,playerrole,interid]
    for i in msglist_trusteeget:
        invest_offer=re.search(repattern_gamemsg,i[0]).group('msgvars').split('#')
        game_rate=re.search(repattern_userinfo,i[1]).group('agentrolevars')
        trusteeget=trusteeget+[[int(invest_offer[0])*int(game_rate[0]),i[2]]]
    #get values that the user repays as trustee
    querycommand_tr="""SELECT gamemsgs.msgbody,playerinfo.interid
                            FROM playerinfo
                            INNER JOIN gamemsgs 
                            ON playerinfo.interid=gamemsgs.interid
                            WHERE(playerinfo.userid=%s
                                AND playerinfo.playerrole LIKE "%s"
                                AND playerinfo.playerrole=gamemsgs.msgsenderrole )
                            ORDER BY playerinfo.interid
                        """%(userid,role)
    msglist_trusteerepay=querymysql(querycommand_tr)
    # calculate final ratio
    for i in msglist_trusteerepay:
        msg_vars=re.search(repattern_gamemsg,i[0]).group('msgvars').split('#')
        trusteerepay=trusteerepay+[[int(msg_vars[0]),i[1]]]
    if len(trusteeget)!=len(trusteerepay):
        print("get len:",len(trusteeget))
        print("repay len:",len(trusteerepay))
        print("repay_num != get_num")
    else:
        for i in range(len(trusteeget)):
            if trusteeget[i][1]==trusteerepay[i][1]:
                trusteerepayratio=trusteerepayratio+[trusteerepay[i][0]/trusteeget[i][0]]
            else:
                print("interid doesn't match")
                break
    return trusteerepayratio

def get_investoroffer_ratio(userid):
    investorofferratio=[]
    role='investor'+'%'
    repattern_gamemsg = re.compile(r'e\((?P<msgname>\w*)\((?P<msgvars>.*)\)\)')
    repattern_userinfo = re.compile(r'(?P<userrolename>\w*)\((?P<agentrolevars>.*)\)')
    #get the user's messages as proposer about offer amount
    querycommand_io="""SELECT gamemsgs.msgbody,playerinfo.playerrole
                            FROM playerinfo
                            INNER JOIN gamemsgs 
                            ON playerinfo.interid=gamemsgs.interid
                            WHERE ( playerinfo.userid=%s 
                                AND playerinfo.playerrole LIKE "%s"
                                AND playerinfo.playerrole=gamemsgs.msgsenderrole )
                        """%(userid,role)
    msglist_investor_sender=querymysql(querycommand_io)
    # extract offer values from the messages
    for i in msglist_investor_sender:
        investor_offer=re.search(repattern_gamemsg,i[0]).group('msgvars').split('#')
        game_total=re.search(repattern_userinfo,i[1]).group('agentrolevars').split(',')
        investorofferratio=investorofferratio+[int(investor_offer[0])/int(game_total[0])]
    return investorofferratio

def get_responderchoice_ratio(userid):
    responderaccept_ratio=[]
    responderreject_ratio=[]
    role='responder'+'%'
    repattern_gamemsg = re.compile(r'e\((?P<msgname>\w*)\((?P<msgvars>.*)\)\)')
    repattern_userinfo = re.compile(r'(?P<userrolename>\w*)\((?P<agentrolevars>.*)\)')
    #get the choice that the responder makes
    querycommand_rc="""SELECT gamemsgs.msgbody,playerinfo.playerrole,playerinfo.interid
                            FROM playerinfo
                            INNER JOIN gamemsgs 
                            ON playerinfo.interid=gamemsgs.interid
                            WHERE ( playerinfo.userid=%s 
                                AND playerinfo.playerrole LIKE "%s"
                                AND playerinfo.playerrole=gamemsgs.msgsenderrole )
                            ORDER BY playerinfo.interid
                        """%(userid,role)
    msglist_responder_send=querymysql(querycommand_rc)#a(acceptornot(accept#3))
    # extract offer values from the messages
    for i in msglist_responder_send:
        responder_msg=re.search(repattern_gamemsg,i[0]).group('msgvars').split('#')
        responder_choice=responder_msg[0]
        proposer_offer=responder_msg[1]
        game_total=re.search(repattern_userinfo,i[1]).group('agentrolevars')
        if responder_choice=="reject":
            responderreject_ratio=responderreject_ratio+[int(proposer_offer)/int(game_total)]
        elif responder_choice=="accept":
            responderaccept_ratio=responderaccept_ratio+[int(proposer_offer)/int(game_total)]
        else:
            print("wired choice!")
    return {'accept':responderaccept_ratio,'reject':responderreject_ratio}

'''
s14_proposeroffer_ratio=get_proposeroffer_ratio(14)
s14_trusteerepay_rartio=get_trusteerepay_ratio(14)
s14_investoroffer_ratio=get_investoroffer_ratio(14)
s14_responderchoice_ratio=get_responderchoice_ratio(14)

print(len(s14_trusteerepay_rartio))
print(len(s14_proposeroffer_ratio))
print(len(s14_investoroffer_ratio))
print(len(s14_responderchoice_ratio['accept'])+len(s14_responderchoice_ratio['reject']))
print("=================")
print(s14_responderchoice_ratio['accept'][0])
print(s14_investoroffer_ratio[0])
print(s14_proposeroffer_ratio[0])
print(s14_trusteerepay_rartio[0])

'''


