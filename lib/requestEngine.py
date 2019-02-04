#This class takes a list of requestObjects and runs the requests
from lib.resultObject import ResultObject
from lib.database import Database
import multiprocessing
from numpy import array_split
import time
import apsw
import requests

class RequestEngine:

    #Initialize our object
    def __init__(self, requestList, dbname, numthread, timeout, 
                    i_size, i_status, display):
        self.requestList = requestList.copy()
        self.rL = requestList.copy()
        self.rLsize = len(self.requestList)
        self.rid = str(time.time())
        self.resp_db = None
        self.req_db = None
        self.display = display
        if dbname != None:
            self.dbname = dbname
            self.resp_db = Database(dbname)
        self.timeout = timeout
        self.numthread = numthread
        self.threads = []
        self.end = multiprocessing.Queue()
        self.q = multiprocessing.Queue() #A queue to hold the response objects
        self.rq_toscan = multiprocessing.Queue() #Requests to be scanned
        self.i_size = i_size             #Response sizes to not store
        self.i_status = i_status         #Response statuses to not store
        
    #Build request Queue and set request IDs
    def build_rq_toscan(self):
        printdata = 'Adding requests to queue: '
        for i in range(0, self.rLsize):
            req = self.requestList.pop(0)
            req.reqID = self.rid+'-'+str(i)
            self.rq_toscan.put(req)
            print(printdata+str(self.rq_toscan.qsize()), end='\r', flush=True)
        print('\nLaunching scanner...')
            

    #This runs our workers
    def run(self):
        self.runtime = str(int(time.time()))
        #Database write threads
        p1 = multiprocessing.Process(target=self.responseToDB)
        self.threads.append(p1)
        
        #endgame thread
        p2 = multiprocessing.Process(target=self.endgame)
        self.threads.append(p2)

        for i in range(0, self.numthread):
            p = multiprocessing.Process(target=self.makereq, args=(i,))
            self.threads.append(p)
        try:
            for p in self.threads:
                p.start()
            for p in self.threads:
                p.join()
        except KeyboardInterrup:
            print('Terminating processes...')
            for p in self.threads:
                p.terminate()
                sys.exit(0)
        self.threads = []

    #How to end the deadlock
    def endgame(self):
        counter = 0
        while True:
            val = self.end.get()
            counter += val
            if counter == self.numthread-1:
                break
        self.q.put(None)
        
    #This functon takes a request object from the queue to process it
    def makereq(self, count):
        rq = requests.session()
        while not self.rq_toscan.empty():
            i = self.rq_toscan.get()
            response = i.request(rq)
            if response != None:
                if(int(response.responseSize) not in self.i_size and
                    int(response.statusCode) not in self.i_status):
                    self.q.put(response)
            time.sleep(self.timeout)
        self.end.put(1)

    #This pops a response off the queue and stores it in the DB
    def responseToDB(self):
        time.sleep(3)
        count = 0
        while True:
            resp = self.q.get()
            if resp == None:
                break
            else:
                if self.resp_db != None:
                    self.resp_db.insert_result(resp)
                    self.requestToDB(resp.respID) #Insert the request
                    count = self.resp_db.get_count()
                no_rq = self.rLsize - self.rq_toscan.qsize()
                printdata = 'Responses: '+ str(count) +'\t\tRequests: '+str(no_rq)
                print(printdata, end='\r', flush=True)
        print('\nScan Completed!')
        if self.dbname != None:
            backupdb = apsw.Connection(self.dbname)
            print('Saving results to '+self.dbname)
            with backupdb.backup("main", self.resp_db.conn, "main") as b:
                while not b.done:
                    b.step(100)
    
    #This stores requests to the DB
    def requestToDB(self, reqID):
            for i in self.rL:
                if reqID == i.reqID:
                    self.resp_db.insert_request(i.get_requestObj())
