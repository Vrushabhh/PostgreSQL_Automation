from encodings.punycode import selective_find

import psycopg2
import pandas as pd
from Utility.ReadWriteExcelSheet import *

import xlsxwriter
import os


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

def execute_query(self,test):
    testdata = pd.read_excel('./testData/Test_Data.xlsx', sheet_name='TestData')
    dynamicTestData = pd.read_excel('./testData/Test_Data.xlsx', sheet_name='DynamicTestData')
    if os.path.isfile('./Reports/Report.xlsx'):
        print('Report.xlsx exists, hence deleting')
        os.remove('./Reports/Report.xlsx')
    workbook = xlsxwriter.Workbook('./Reports/Report.xlsx')
    BoldandColor = workbook.add_format({'bold': True, 'bg_color': 'yellow'})
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', 'Queries',BoldandColor)
    worksheet.write('B1', 'Response',BoldandColor)
    worksheet.write('C1', 'Result', BoldandColor)
    workbook.close()
    conn = database_connection(test)
    cursor = conn.cursor()
    query = testdata['Query']
    userIDs=dynamicTestData['UserId']
    print('Total SQL Queries :- ', query.__len__())
    l=1
    for i in query:
        if 'userId' in i:
            for j in userIDs:
                k=i.replace('userId',j)
                print('Executing Query :- \n', k)
                cursor.execute(k)
                record = cursor.fetchone()
                print('Query Output :- \n', record)
                queryColumn = 1
                responseColumn = 2
                resultColumn = 3

                if record is None:
                    print("No record found")
                    ReadExcel.WriteExcel(self, "./Reports/Report.xlsx", "Sheet1", l + 1, queryColumn,
                                         k)
                    ReadExcel.WriteExcel(self, "./Reports/Report.xlsx", "Sheet1", l + 1, responseColumn,
                                         str(record))
                    ReadExcel.WriteExcel(self,"./Reports/Report.xlsx", "Sheet1", l + 1,resultColumn, "No Record Found")
                    ReadExcel.RedBgrColor(self,"./Reports/Report.xlsx","Sheet1",l + 1,resultColumn)
                    l=l+1
                else:
                    print("Records found")
                    ReadExcel.WriteExcel(self, "./Reports/Report.xlsx", "Sheet1", l + 1, queryColumn,
                                         k)
                    ReadExcel.WriteExcel(self, "./Reports/Report.xlsx", "Sheet1", l + 1, responseColumn,
                                         str(record))
                    ReadExcel.WriteExcel(self, "./Reports/Report.xlsx", "Sheet1", l+ 1,resultColumn, "Pass")
                    ReadExcel.GreenBgrColor(self,"./Reports/Report.xlsx", "Sheet1", l + 1,resultColumn)
                    l=l+1
        else:
            print('Executing Query :- \n',i)
            cursor.execute(i)
            record = cursor.fetchone()
            print('Query Output :- \n',record)
            queryColumn = 1
            responseColumn = 2
            resultColumn = 3
            if record is None:
                print("No record found")
                ReadExcel.WriteExcel(self, "./Reports/Report.xlsx", "Sheet1", l + 1, queryColumn,
                                     k)
                ReadExcel.WriteExcel(self, "./Reports/Report.xlsx", "Sheet1", l + 1, responseColumn,
                                     str(record))
                ReadExcel.WriteExcel(self,"./Reports/Report.xlsx", "Sheet1", l + 1,resultColumn, "No Record Found")
                ReadExcel.RedBgrColor(self,"./Reports/Report.xlsx", "Sheet1", l + 1,resultColumn)
                l=l+1
            else:
                print("Records found")
                ReadExcel.WriteExcel(self, "./Reports/Report.xlsx", "Sheet1", l + 1, queryColumn,
                                     i)
                ReadExcel.WriteExcel(self, "./Reports/Report.xlsx", "Sheet1", l + 1, responseColumn,
                                     str(record))
                ReadExcel.WriteExcel(self,"./Reports/Report.xlsx", "Sheet1", l+1,resultColumn, 'Pass')
                ReadExcel.GreenBgrColor(self,"./Reports/Report.xlsx", "Sheet1", l + 1,resultColumn)
                l=l+1
    return record