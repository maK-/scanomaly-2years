#This class represents a request
#It stores various properties of a request and returns a response object
import requests
import time
import copy
import urllib3
from re import findall
from lib.resultObject import ResultObject

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class RequestObject:

    #Initialize a Request object 
    def __init__(self, reqID, method, proxy, headers, timeout, cookies,
                    url, data, module):
        self.reqID = reqID
        self.method = method
        self.proxy = proxy
        self.headers = headers
        self.timeout = timeout
        self.cookies = cookies
        self.url = url
        self.data = data
        self.module = module

    #Get request object data for DB
    def get_requestObj(self):
        self.req_data = {
                            "reqID": str(self.reqID),
                            "method": str(self.method),
                            "proxy": str(self.proxy),
                            "headers": str(self.headers),
                            "cookies": str(self.cookies),
                            "url": str(self.url),
                            "data": str(self.data),
                            "module": str(self.module)
                        }
        return self.req_data

    #Make a request
    def request(self, session):
        self.startTime = time.time()
        r = session
        rq = '' #Temporarily store request response
        resp_data = {
                            "respID": str(self.reqID),
                            "responseSize": str(-1),
                            "statusCode": str(-1),
                            "time": str(-1),
                            "numHeaders": str(-1),
                            "numTokens": str(-1),
                            "headers": str(-1)
                    } 
        try:
            if self.method == 'GET':
                rq = r.get(self.url, timeout=self.timeout, 
                                verify=False, allow_redirects=False,
                                headers=self.headers, cookies=self.cookies,
                                proxies=self.proxy)
            elif self.method == 'POST':
                rq = r.post(self.url, timeout=self.timeout, 
                                verify=False, allow_redirects=False,
                                headers=self.headers, cookies=self.cookies,
                                proxies=self.proxy)
            elif self.method == 'PUT':
                rq = r.put(self.url, timeout=self.timeout,
                                verify=False, allow_redirects=False,
                                headers=self.headers, cookies=self.cookies,
                                 proxies=self.proxy)
            elif self.method == 'PATCH':
                rq = r.patch(self.url, timeout=self.timeout,
                                verify=False, allow_redirects=False,
                                headers=self.headers, cookies=self.cookies,
                                proxies=self.proxy)
            elif self.method == 'DELETE':
                rq = r.delete(self.url, timeout=self.timeout,
                                verify=False, allow_redirects=False,
                                headers=self.headers, cookies=self.cookies,
                                proxies=self.proxy)
            elif self.method == 'OPTIONS':
                rq = r.options(self.url, timeout=self.timeout,
                                verify=False, allow_redirects=False,
                                headers=self.headers, cookies=self.cookies,
                                proxies=self.proxy)
            elif self.method == 'HEAD':
                rq = r.head(self.url, timeout=self.timeout,
                                verify=False, allow_redirects=False,
                                headers=self.headers, cookies=self.cookies,
                                proxies=self.proxy)
            else:
                rq = r.request(self.method, self.url, timeout=self.timeout,
                                verify=False, allow_redirects=False,
                                headers=self.headers, cookies=self.cookies,
                                proxies=self.proxy)
            resp_data = {
                            "respID": str(self.reqID),
                            "responseSize": str(len(rq.content)),
                            "statusCode": str(rq.status_code),
                            "time": str((time.time() - self.startTime)),
                            "numHeaders": str(len(rq.headers)),
                            "numTokens": str(len(findall(r'\w+', rq.text))),
                            "headers": str(rq.headers)
                        }
        except requests.exceptions.Timeout:
            resp_data['statusCode'] = '-1'
            pass
        except requests.exceptions.ConnectionTimeout:
            resp_data['statusCode'] = '-2'
            pass
        except requests.exceptions.ConnectionError:
            resp_data['statusCode'] = '-3'
            pass
        except requests.exceptions.TooManyRedirects:
            resp_data['statusCode'] = '-4'
            pass
        
        try:
            #Create a result Object
            self.responseObj = ResultObject(resp_data['respID'], 
                                            resp_data['responseSize'],
                                            resp_data['statusCode'],
                                            resp_data['time'], 
                                            resp_data['numHeaders'],
                                            resp_data['numTokens'])
        except:
            print('Exception: '+self.reqID)
        return self.responseObj


