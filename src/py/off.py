#!/usr/bin/python

'''Log out cgi'''

from __future__ import print_function
import Cookie
import sys
sys.path.insert(0, "/var/www/yagra/config")
from common import HOST_NAME

cookie = Cookie.SimpleCookie()
cookie['session'] = 'nobody|nothing'
cookie['session']['path'] = '/yagra'
cookie['session']['httponly'] = 1
print(cookie.output())
print('Location: http://%s/yagra' % (HOST_NAME))
print()
