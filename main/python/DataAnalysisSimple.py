import DataTransferMySQLSimple

gamedata=DataTransferMySQLSimple.datatransferMySQL("localhost")

offerratio=[]
for i in range(len(gamedata)):
    if (gamedata[i]['protocolid']=='ultimategame' and gamedata[i]['role']['rname']=='proposer'):
        wholeamount=gamedata[i]['role']['rvars'][0]
        for j in range(len(gamedata[i]['messages'])):
            if gamedata[i]['messages'][j]['mname']=='offer':
                theratio=float(gamedata[i]['messages'][j]['mvars'][0])/float(wholeamount)
        offerratio=offerratio+[theratio,]
print "proposer's offerratio is %s" %offerratio

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
print "responder's acceptratio is %s" %acceptratio
print "responder's rejectratio %s" %rejectratio

investratio=[]
for i in range(len(gamedata)):
    if (gamedata[i]['protocolid']=='trustgame_simple' and gamedata[i]['role']['rname']=='investor'):
        investorown=gamedata[i]['role']['rvars'][0]
        for j in range(len(gamedata[i]['messages'])):
            if gamedata[i]['messages'][j]['mname']=='offer':
                theratio=float(gamedata[i]['messages'][j]['mvars'][0])/float(investorown)
        investratio=investratio+[theratio,]
print "investor's investratio is %s" %investratio 

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
print "trustee's repayratio is %s" %repayratio

