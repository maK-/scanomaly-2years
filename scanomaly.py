#!/usr/bin/env python3
import sys
import argparse
import time
import os
from lib.requestObject import RequestObject
from lib.agentObject import UserAgent
from lib.requestEngine import RequestEngine
from lib.version import VersionInfo
from lib.dataparser import ParseArguments
from lib.fileOp import FileOp
from lib.database import Database
from yapsy.PluginManager import PluginManager
from colored import fg, bg, attr

rs = attr('reset')

if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument('-p', '--proxy', type=str, default=None,
                        help=fg(8)+'Use a proxy (http|s://[ip]:[port])'+rs)
    parse.add_argument('-P', '--printed', action='store_true', default=False,
                        help=fg(8)+'Print all results at end'+rs)
    parse.add_argument('-a', '--agent', type=str, default='Scanomalie v2.0',
                        help=fg(8)+'Specify a user agent'+rs)
    parse.add_argument('-al', '--agentlist', action='store_true', default=False,
                        help=fg(8)+'Use random agent from list'+rs)
    parse.add_argument('-ar', '--agentran', action='store_true', default=False,
                        help=fg(8)+'Randomise agent every request'+rs)
    parse.add_argument('-H', '--headers', nargs='+',
                        help=fg(8)+'Add headers in format "a:b" "c:d"'+rs)
    parse.add_argument('-c', '--cookie', type=str, default=None,
                        help=fg(8)+'Specify Cookies'+rs)
    parse.add_argument('-d', '--data', type=str, default=None,
                        help=fg(8)+'Specify data like a=b&c=d (GET params)'+rs)
    parse.add_argument('-dl', '--datalist', nargs='+',
                        help=fg(8)+'Pass lists to use'+rs)
    parse.add_argument('-db', '--database', type=str, default=None,
                        help=fg(8)+'Specify a database to use'+rs)
    parse.add_argument('-T', '--timeout', type=int, default=10,
                        help=fg(8)+'Seconds to wait for response'+rs)
    parse.add_argument('-tt', '--requestTimeout', type=int, default=0,
                        help=fg(8)+'Seconds to wait between each request'+rs)
    parse.add_argument('-s', '--ignoresize', nargs='+', default=[],
                        help=fg(8)+'Ignore response of size (26 12345 350)'+rs)
    parse.add_argument('-x', '--ignorestatus', nargs='+', default=[404],
                        help=fg(8)+'Specify status to ignore (503 400 500)'+rs)
    parse.add_argument('-v', '--version', action='store_true', default=False,
                        help=fg(8)+'Display Version information'+rs)
    parse.add_argument('-u', '--url', type=str, default=None,
                        help=fg(8)+'Specify a URL to use'+rs)
    parse.add_argument('-ul', '--urlist', type=str, default=None,
                        help=fg(8)+'Specify a list of URLs'+rs)
    parse.add_argument('-m', '--modules', nargs='+',
                        help=fg(8)+'Pass generational modules to use'+rs)
    parse.add_argument('-mi', '--modinfo', action='store_true', default=False,
                        help=fg(8)+'Print Information about a module'+rs)
    parse.add_argument('-mx', '--modexcl', nargs='+', default=[],
                        help=fg(8)+'List modules to exclude'+rs)
    parse.add_argument('-t', '--threads', type=int, default=2,
                        help=fg(8)+'Specify number of threads to use'+rs)
    parse.add_argument('-scan', '--scans', action='store_true', default=False,
                        help=fg(8)+'Run a scan'+rs)
    
    args = parse.parse_args()

    #Variables for requests
    total_headers = {}
    cookies = {}
    proxies = {}
    data = {}
    timeout = args.timeout
    total_headers.update({'User-Agent':args.agent})
    ReqList = []        

    #Current working directory
    cwd = os.getcwd()  

    #If no arguments display help
    if len(sys.argv) <= 1:
        version = VersionInfo(2.0)
        version.show()
        parse.print_help()
        sys.exit(0)

    #Display version information
    if args.version == True:
        version = VersionInfo(2.0)
        version.show()

    #Add user supplied headers
    if args.headers != None:
        head = ParseArguments()
        head.parseHeaders(args.headers)
        headers = head.parseHeaders(args.headers)
        for i in headers:
            total_headers.update({i:headers[i]})

    #Add user supplied cookies
    if args.cookie != None:
        cookie = ParseArguments()
        cookies = cookie.parseCookies(args.cookie)

    #Add user supplied proxy
    if args.proxy != None:
        proxy = ParseArguments()
        proxies = proxy.parseProxy(args.proxy)

    #Add user supplied data
    if args.data != None:
        dataarg = ParseArguments()
        datas = dataarg.parseData(args.data)
        if len(datas) > 0:
            for i in datas:
                data.update({i:datas[i]})
        else:
            data = ''

    #Load the Modules
    if args.modules != None:
        run_mods = []
        
        #Creating our plugin manager
        manager = PluginManager()
        manager.setPluginPlaces(["modules"])
        manager.collectPlugins()
        
        #Get all plugins
        if "all" in args.modules:
            run_mods = manager.getAllPlugins()
        else:
            #Load plugins listed
            for i in args.modules:
                run_mods.append(manager.getPluginByName(i))
        
        #Print Module info
        if(args.modinfo):
            for i in run_mods:
                if i.name not in args.modexcl:
                    print(fg(8)+'---'+fg(1)+i.name+fg(8)+'---'+rs)
                    print(fg(8)+'Description: '+rs+i.description)
                    print(fg(8)+'Author: '+rs+i.author)
                    print(fg(8)+'Website: '+rs+i.website)
                    print('')

    
    #URLs to use with modules
    if ((args.url != None and args.modules != None) or 
            (args.urlist != None and args.modules != None)):
        urls = []   
        
        #Get URL from CLI
        if args.url != None:    
            urldata = ParseArguments()
            newdata = urldata.parseUrlData(args.url)
            if len(newdata) > 0:
                for i in newdata:
                    data.update({i:newdata[i]})
            if '?' in args.url:
                args.url = args.url.split('?')[0]
            args.url += urldata.parseUrlfromData(data)
            urls = [args.url]

        #GET URLS from file
        if args.urlist != None:
            urlist = FileOp(args.urlist).reader()
            urls = urls + urlist
        
        print('Urls: '+fg(1)+str(len(urls))+rs)
        print(fg(8)+'---'+rs+'Loading Modules'+fg(8)+'---'+rs)

        #Add RequestObjects to list
        #New modules need to be added to this section with their arguments
        #To add user CLI input use args.datalist (allows a list of arguments)
        #Using -dl data1 data2 (specify strings or files etc)
        #======================================================================
        results = []
        for z in run_mods:
            if z != None:
                #If the module name matches - pass the right arguments to gen
                if z.name == 'repo':
                    if z.name not in args.modexcl:
                        results = z.plugin_object.gen(cwd, urls, proxies, 
                                                        total_headers, timeout, 
                                                        cookies, data, z.name)
                if z.name == 'archives':
                    if z.name not in args.modexcl:
                        results = z.plugin_object.gen(cwd, urls, proxies, 
                                                        total_headers, timeout, 
                                                        cookies, data, z.name)
                if z.name == 'parameth':
                    if z.name not in args.modexcl:
                        results = z.plugin_object.gen(cwd, urls, proxies, 
                                                        total_headers, timeout, 
                                                        cookies, data, z.name)
                if z.name == 'dirb': 
                    if z.name not in args.modexcl:
                        results = z.plugin_object.gen(cwd, urls, proxies, 
                                                        total_headers, timeout, 
                                                        cookies, data, z.name)
                if z.name == 'dirb-files': 
                    if z.name not in args.modexcl:
                        results = z.plugin_object.gen(cwd, urls, proxies, 
                                                        total_headers, timeout, 
                                                        cookies, data, z.name, 
                                                        args.datalist)
                if z.name == 'vhost':
                    if z.name not in args.modexcl:
                        results = z.plugin_object.gen(cwd, urls, proxies, 
                                                        total_headers, timeout, 
                                                        cookies, data, z.name,
                                                        args.datalist)
        #======================================================================        
                if z.name not in args.modexcl:
                    print('Module: '+fg(1)+str(z.name)+rs)
                    print('Imported: '+fg(1)+str(len(results))+rs)
                    print(fg(8)+'---------------------'+rs)
                    for rq in results:
                        ReqList.append(rq)
        print('Total Requests to make: '+fg(2)+str(len(ReqList))+rs)

    #Change all requests in list to random agent
    if args.agentlist == True and ReqList != None:
        ua = UserAgent(ReqList)
        ReqList = ua.agentlist()

    #Change all requests to random agents
    if args.agentran == True and ReqList != None:
        ua = UserAgent(ReqList)
        ReqList = ua.agentran()

    #Run Scan
    if args.scans == True and ReqList != None:
        r_engine = RequestEngine(ReqList, args.database, args.threads, 
                                    args.requestTimeout, args.ignoresize, 
                                    args.ignorestatus, args.printed)
        r_engine.build_rq_toscan()
        r_engine.run()
