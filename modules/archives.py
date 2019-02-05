#This module is used to find common file archives
from yapsy.IPlugin import IPlugin
from lib.requestObject import RequestObject
from lib.fileOp import FileOp
from lib.dataparser import ParseArguments
from lib.urlObject import UrlObject
import random

class Archives(IPlugin):

    def __init__(self):
        self.requestList = [] #Store generated request objects
        self.prepend =  [
                        '_','.','~','%20','-','.~','Copy%20of%20',
                        'copy%20of%20','Copy_','Copy%20','Copy_of_',
                        'Copy_(1)_of_','%24',
                        ]
        self.common =   [
                        'www', 'html', 'public', 'public_html', 'web',
                        'wwwroot', 'website', 'root', 'src', 'source', 
                        'data', 'dir', 'site', 'index', 'htdoc', 'htdocs'
                        ]

    def gen(self, cwd, urls, proxy, headers, timeout, cookies, postdata, 
            module):
        d1 = ''
        d2 = ''
        self.data = FileOp(cwd+'/lists/archive-file.txt').reader()
        for url in urls:
            u = UrlObject(url)

            #If no lastfile
            if u.lastfile != '':
                for i in self.data:
                    d1 = u.u_q + i
                    req_get = RequestObject('reqID',"GET", proxy, headers, 
                                            timeout, cookies, d1, postdata,
                                            module)
                    self.requestList.append(req_get)

                    d2 = u.u_d + u.lastfile_ext+i
                    req_get = RequestObject('reqID',"GET", proxy, headers,
                                            timeout, cookies, d2, postdata, 
                                            module)
                    self.requestList.append(req_get)

                for i in self.prepend:
                    d1 = u.u_d + i + u.lastfile
                    req_get = RequestObject('reqID',"GET", proxy, headers,
                                            timeout, cookies, d1, postdata,
                                            module)
                    self.requestList.append(req_get)
                    
                    for j in self.data:
                        d2 = u.u_d + i + u.lastfile + j
                        req_get = RequestObject('reqID',"GET", proxy, headers, 
                                            timeout, cookies, d2, postdata,
                                            module)
                        self.requestList.append(req_get)

            #If no lastpath    
            if u.lastpath != '':
                for i in self.data:
                    d1 = u.u_d + u.lastpath + i
                    req_get = RequestObject('reqID',"GET", proxy, headers, 
                                            timeout, cookies, d1, postdata,
                                            module)
                    self.requestList.append(req_get)
                    d2 = u.u_dd + u.lastpath + i
                    req_get = RequestObject('reqID',"GET", proxy, headers, 
                                            timeout, cookies, d2, postdata,
                                            module)
                    self.requestList.append(req_get)
                for i in self.common:
                        for j in self.data:
                                d1 = u.u_d + i + j
                                req_get = RequestObject('reqID',"GET", proxy, headers, 
                                            timeout, cookies, d1, postdata,
                                            module)
                                self.requestList.append(req_get)
            #Else
            else:
                for i in self.common:
                    for j in self.data:
                        d1 = u.u_d + i + j
                        req_get = RequestObject('reqID',"GET", proxy, headers, 
                                            timeout, cookies, d1, postdata,
                                            module)
                        self.requestList.append(req_get)

        return self.requestList
