import mysql.connector as connector

global con, cur
con = connector.connect(host='localhost', port='3306', user='root', password='root', database='rvcedatabase')
cur = con.cursor()


def createTables():
    queries = [
        "create table if not exists logininfo(username varchar(50) primary key, password varchar(200))",
        "create table if not exists prompts(username varchar(50), prompt varchar(200), feedback int)"
    ]
    for query in queries:
        cur.execute(query)
        print("OK ", query)


def addLogin(username, password):
    query = f'insert into logininfo values("{username}","{password}")'
    cur.execute(query)
    con.commit()


def addPrompt(username, prompt, feedback):
    query = f'insert into prompts values("{username}","{prompt}",{feedback})'
    cur.execute(query)
    con.commit()


def checkLogin(username):  # To check is user exists or not
    query = f'select * from logininfo where username = "{username}"'
    cur.execute(query)
    val = ""
    for row in cur:
        val = row[0]
    if val == "":
        return 'UserDoesNotExist'
    else:
        return 'UserExists'


def checkPassword(username, password):  # To check is user's password
    query = f'select * from logininfo where username = "{username}"'
    cur.execute(query)
    passw = ""
    for row in cur:
        passw = row[1]
    if password == passw:
        return 'True'
    else:
        return 'False'