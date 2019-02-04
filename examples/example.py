#This is an example module
"""
* The goal of a module is to generate requests to be carried out        *
* There are multiple libraries available to speed up this process.      *
* Many arguments are passed from the command line. The goal is rapid    *
* creation and proof of concepting fuzzing ideas.                       *
*                                                                       *
* `-dl` This allows strings to be passed to modules via the CLI         *
*       Strings could be filenames or commands to be used for           *
*        instructing the module. The datalist parameter is a list.      *
*                                                                       *
* A module returns a list of RequestObjects.                            *
"""
#=========================
from yapsy.IPlugin import IPlugin          
from lib.requestObject import RequestObject
from lib.urlObject import UrlObject
from lib.fileOp import FileOp

class Example(IPlugin):
    """
        This Example module performs a request of each request method
        =============================================================
        cwd = current working directory
        urls = list of urls
        proxy = proxy information for request
        headers = header dictionary for request
        timeout = timeout for request
        cookies = cookies used for request
        postdata = parameters and data
        moduele = name of the module
    """
    def gen(self, cwd, urls, proxy, headers, timeout, cookies, postdata, 
            module):
        requestList = []   #Store generated request objects
        requestMethods = ['GET','POST','OPTIONS','HEAD','PUT','DELETE','PATCH']
        
        for i in urls:
            for j in requestMethods:
                req_get = RequestObject('reqID', j, proxy, headers, timeout, 
                                        coookies, i, postdata, module)
        requestList.append(req_get)
        return requestList
