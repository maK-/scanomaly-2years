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

        """
        *   The baseline request will later be used for smarter things
        *   For example auto ignoring status codes or certain sizes
        *   or a baseline for our AI to detect anomalies.
        """

        for url in urls:
            #Standard baseline request
            req_get = RequestObject('reqID', 'GET', proxy, headers, timeout,
                                        cookies, url, postdata, module)
            requestList.append(req_get)

            #Does our response size change for each request?
            req_get = RequestObject('reqID', 'GET', proxy, headers, timeout,
                                        cookies, url, postdata, module)
            requestList.append(req_get)

            #Baseline of a 404 dir
            url404 = url + self.tenstr
            req_get = RequestObject('reqID', 'GET', proxy, headers, timeout,
                                        cookies, url404, postdata, module)
            requestList.append(req_get)

            #Different for a file?
            url404 = url + self.tenstr + '.html'
            req_get = RequestObject('reqID', 'GET', proxy, headers, timeout,
                                        cookies, url404, postdata, module)
            requestList.append(req_get)

            #Baseline of large 404 (is url reflected in body?)
            url404lrg = url + self.hundredstr
            req_get = RequestObject('reqID', 'GET', proxy, headers, timeout,
                                        cookies, url404lrg, postdata, module)
            requestList.append(req_get)

        return requestList
