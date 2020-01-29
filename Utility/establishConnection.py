import psycopg2
import pandas as pd

def database_connection(test):
    print('Executing Test :- ',test)
    global connection
    try:
        testdata = pd.read_excel('./testData/Test_Data.xlsx',sheet_name='DB_Connection')
        hostname = testdata['Host']
        username = testdata['Username']
        password = testdata['Password']
        port = testdata['Port']
        database = testdata['Database']

        connection = psycopg2.connect(user = username[0],
                                  password = password[0],
                                  host = hostname[0],
                                  port = port[0],
                                  database = database[0])
        print('PostgreSQL Connection Established Successfully')
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    return connection

def execute_query(test):
    testdata = pd.read_excel('./testData/Test_Data.xlsx', sheet_name='TestData')
    conn = database_connection(test)
    cursor = conn.cursor()
    query = testdata['Query']
    print('Total SQL Queries :- ', query.__len__())
    for i in query:
        print('Executing Query :- \n',i)
        cursor.execute(i)
        record = cursor.fetchone()
        print('Query Output :- \n',record)
    return record
