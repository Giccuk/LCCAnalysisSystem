import mysql.connector


def querymysql(query_command,dbconfig):
    db=mysql.connector.connect(host=dbconfig[0],
                           database=dbconfig[1],
                           user=dbconfig[2],
                           password=dbconfig[3])
    cursor=db.cursor()
    cursor.execute(query_command)
    queryresult=cursor.fetchall()
    cursor.close()
    db.close()
    return queryresult

userid=14
lccgameconfig=['localhost','lccgame','host','host']

query="SELECT * FROM lccengine WHERE COMM_ID='INT7254'"
interdata_raw=querymysql(query,lccgameconfig)
interdata=[x for x in interdata_raw[0] if x!='']


interdata_list=[]
for j in interdata_raw[0]:
    interdata_list.append(j)


new_interlist = []
for i in range(len(interdata_list)):
    if i != '':
        new_interlist.append(interdata_list[i].replace('p12', 'p13'))
    else:
        new_interlist.append(interdata_list[i])

insertquery = """INSERT INTO lccengine VALUES ('%s','%s','%s','%s','%s','%s','%s')""" % (new_interlist[0],
                                                                                         new_interlist[1],
                                                                                         new_interlist[2],
                                                                                         new_interlist[3],
                                                                                         new_interlist[4],
                                                                                         new_interlist[5],
                                                                                         new_interlist[6]
                                                                           )

print(insertquery)

db = mysql.connector.connect(host="localhost",
                             database='lccgame',
                             user='host',
                             password='host')
cursor = db.cursor()
cursor.execute(insertquery)
db.close()






