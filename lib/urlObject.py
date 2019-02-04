import string
from urllib.parse import urlparse

'''
Url Object for easier parsing ( http://x.com/demo/test.html?x=1 )
====================================================

u.u_d = current url to last dir (http://x.com/demo/)
u.u_dd = current url to last dir -1
u.u_q = current url without query string (http://x.com/demo/test.html)
u.full = full url (http://x.com/demo/test.html?x=1)
u.query = full query (x=1)
u.lastpath = name of last directory (demo)
u.lastfile = last file (test.html)
u.lastfile_ext = last file without extension (test)
'''

class UrlObject:
    def __init__(self, url):
        self.u = urlparse(url)
        self.u_q = self.u[0]+'://'+self.u[1]+self.u[2]
        self.full = self.u.geturl()
        self.query = self.u[4]
        self.lastpath = ''
        self.lastfile = ''
        self.lastfile_ext = ''
        self.u_dd = ''
        if '/' in self.u[2]:
            self.path = self.u[2].split('/')
            self.lenpath = len(self.path)-1
            if self.lenpath != 1 or self.lenpath != 0:
                if '.' in self.path[self.lenpath]:
                    self.lastfile = self.path[self.lenpath]
                    self.path.pop(self.lenpath)
                self.lastpath = self.path[self.lenpath-1]
                tmp = self.u[0]+'://'+self.u[1]+'/'.join(self.path)
                if tmp.endswith('/'):
                    self.u_d = tmp
                else:
                    self.u_d = tmp + '/'
            else:
                self.u_d = self.u[0]+'://'+self.u[1]+self.u[2]
                self.lastpath = ''
                self.lastfile = self.u_q.split('/')[-1:]
        else:
            self.u_d = self.u[0]+'://'+self.u[1]+self.u[2]
            self.lastpath = ''
            self.lastfile = self.u_q.split('/')[-1:]
        
        if '.' in self.lastfile:
            self.lastfile_ext = self.lastfile.split('.')[0]
        if self.lastpath != '':
            tmp = self.lastpath+'/'
            tmp2 = self.u_d.split(tmp)
            if len(tmp2) == 2:
                self.u_dd = tmp2[0]
            else:
                tmp2.pop(len(tmp2)-1)
                self.u_dd = tmp.join(tmp2)	
