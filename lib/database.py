#This class is used to store response objects
import apsw
from lib.resultObject import ResultObject
from colored import fg, bg, attr

class Database:

    #Initialize the database
    def __init__(self, dbfile):
        self.dbfile = dbfile
        self.conn = apsw.Connection(':memory:')
        self.cursor = self.conn.cursor()
        self.rs = attr('reset')

        #Create Database tables
        create = 'CREATE TABLE IF NOT EXISTS responses('
        create += 'timestamp datetime default current_timestamp,'
        create += 'respID text NOT NULL,'
        create += 'responseSize text NOT NULL,'
        create += 'statusCode text NOT NULL,'
        create += 'time text NOT NULL,'
        create += 'numHeaders text NOT NULL,'
        create += 'numTokens text NOT NULL)'
        self.cursor.execute(create)

        create = 'CREATE TABLE IF NOT EXISTS requests('
        create += 'reqID text NOT NULL,'
        create += 'method text NOT NULL,'
        create += 'proxy text NOT NULL,'
        create += 'headers text NOT NULL,'
        create += 'cookies text NOT NULL,'
        create += 'url text NOT NULL,'
        create += 'data text NOT NULL,'
        create += 'module text NOT NULL)'
        self.cursor.execute(create)
    
    #Insert response Object into database
    def insert_result(self, resObj):
        data = {
                    "respID": str(resObj.respID),
                    "responseSize": str(resObj.responseSize),
                    "statusCode": str(resObj.statusCode),
                    "time": str(resObj.time),
                    "numHeaders": str(resObj.numHeaders),
                    "numTokens": str(resObj.numTokens),
                }
        insert = 'INSERT INTO responses(respID,responseSize,statusCode,time,'
        insert += 'numHeaders,numTokens) VALUES (:respID,:responseSize,'
        insert += ':statusCode,:time,:numHeaders,:numTokens)'
        try:
            self.cursor.execute(insert, data)
        except apsw.OperationalError:
            print('SQL Error: insert_result')

    #Insert request Object
    def insert_request(self, reqObj):
        insert = 'INSERT INTO requests(reqID,method,proxy,headers,cookies,'
        insert += 'url,data,module) VALUES (:reqID,:method,:proxy,:headers,'
        insert += ':cookies,:url,:data,:module)'
        try:
            self.cursor.execute(insert, reqObj)
        except apsw.OperationalError:
            print('SQL Error: insert request')

    #Get number of entries
    def get_count(self):
        select = 'SELECT COUNT(*) FROM responses'
        try:
            self.cursor.execute(select)
            results = self.cursor.fetchone()
            return results[0]
        except apsw.OperationalError:
            print('SQL Error: get_count')
            pass

    #Get response IDs
    def get_responses(self):
        respdata = []
        select = 'SELECT respID FROM responses'
        try:
            self.cursor.execute(select)
            resps = self.cursor.fetchall()
            for i in resps:
                respdata.append(i[0])
            return respdata
        except apsw.OperationalError:
            print('SQL Error: get responses')

    def return_all(self):
        select = 'SELECT requests.module, requests.url, responses.responseSize,'
        select += ' responses.statusCode, responses.time, responses.numHeaders,'
        select += ' responses.numTokens FROM requests '
        select += 'INNER JOIN responses ON responses.respID == requests.reqID'
        try:
            self.cursor.execute(select)
            resps = self.cursor.fetchall()
            forprint = fg(1)+'Module: '+fg(8)+'URL '+fg(4)+'status '+fg(10)
            forprint += 'size '+fg(3)+'time '+fg(13)+'numHeaders '+fg(14)
            forprint += 'numTokens'+self.rs
            print(forprint)
            for i in resps:
                response = fg(1)+i[0]+self.rs+': '+fg(8)+i[1]+' '+fg(4)+i[3]
                response += ' '+fg(10)+i[2]+' '+fg(3)+i[4]+' '+fg(13)+i[5]+' '
                response += fg(14)+i[6]+self.rs
                print(response)
        except apsw.OperationalError:
            print('SQL Error: return all')
        return
            

    #Close the database connection
    def close(self):
        self.conn.close()        
