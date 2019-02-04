#This module is used to brute force parameters
from yapsy.IPlugin import IPlugin
from lib.requestObject import RequestObject
from lib.fileOp import FileOp
from lib.dataparser import ParseArguments
from lib.urlObject import UrlObject

class Parameth(IPlugin):

    def getParamStr(self, reqdata):
        dataString = ''
        if len(reqdata) != 0:
            for i,j in reqdata.items():
                dataString += i + '=' + j
                dataString += '&'
        return dataString[:-1]

    def gen(self, cwd, urls, proxy, headers, timeout, cookies, postdata, 
            module):
        requestList = []   #Store generated request objects
        data = FileOp(cwd+'/lists/parameters.txt').reader()
        paramValue = 'discobiscuits'
        db = ''
        for url in urls:
            u = UrlObject(url)
            for param in data:
                ndata = postdata.copy()
                ndata[param] = paramValue
                db = u.u_q + '?' + self.getParamStr(ndata)
                req_get = RequestObject('reqID',"GET", proxy, headers, timeout,
                                            cookies, db, ndata, module)
                requestList.append(req_get)
                req_post = RequestObject('reqID',"POST", proxy, headers,timeout,
                                            cookies, u.u_q, ndata, module)
                requestList.append(req_post)
                del ndata[param]
        return requestList
