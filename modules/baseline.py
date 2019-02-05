#This module gets request baselines
#=========================
from yapsy.IPlugin import IPlugin          
from lib.requestObject import RequestObject
from lib.urlObject import UrlObject
from lib.fileOp import FileOp
import random
import string

class Baseline(IPlugin):

    def __init__(self):
        self.strings = string.ascii_uppercase
        self.strings += string.ascii_lowercase
        self.strings += string.digits
        self.tenstr = ''.join(random.choices(self.strings, k=10))
        self.hundredstr = ''.join(random.choices(self.strings, k=100))

    def gen(self, cwd, urls, proxy, headers, timeout, cookies, postdata, 
            module):
        requestList = []   #Store generated request objects
        requestMethods = ['GET','POST','OPTIONS','HEAD','PUT','DELETE','PATCH']
        
        for url in urls:
            for j in requestMethods:
                req_get = RequestObject('reqID', j, proxy, headers, timeout, 
                                        cookies, url, postdata, module)
                requestList.append(req_get)

        for url in urls:
            #Does our response size change for each request?
            req_get = RequestObject('reqID', 'GET', proxy, headers, timeout,
                                        cookies, url, postdata, module)
            requestList.append(req_get)

            #Baseline of a 404 page
            url404 = url + self.tenstr
            req_get = RequestObject('reqID', 'GET', proxy, headers, timeout,
                                        cookies, url404, postdata, module)
            requestList.append(req_get)

            #Baseline of large 404 (is url reflected in body?)
            url404lrg = url + self.hundredstr
            req_get = RequestObject('reqID', 'GET', proxy, headers, timeout,
                                        cookies, url404lrg, postdata, module)
            requestList.append(req_get)

        return requestList
