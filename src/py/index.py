#!/usr/bin/python

'''cgi for work as index'''
from __future__ import print_function
import sys

sys.path.insert(0, "/var/www/yagra/config")

import os
from sys import stderr
from common import ERROR_PAGE_URL
from common import HOST_NAME
from common import TEMPLATE_PATH
from common import login_user

try:
    template = ''
    with open(TEMPLATE_PATH + '/main.html') as fh: template = fh.read()
    username = login_user()

    if username is not None:
        print('Content-Type: text/html')    # HTML is following
        print()
        print(template % ('http://%s/yagra/upload/' % (HOST_NAME), username,
            '<li><a href="/yagra/off.py">Sign out</a></li>',
            'http://%s/yagra/upload/' % (HOST_NAME), 'Upload New Avatar'))
    else: # not login
        print('Content-Type: text/html')    # HTML is following
        print()
        print(template % ('http://%s/yagra/sign_in/' % (HOST_NAME), 'Sign in',
            '', 'http://%s/yagra/sign_up/' % (HOST_NAME), 'Sign Up now'))
except Exception as e:
    print('Something wrong: {0}'.format(e), file=stderr)
    print('Location: %s' % (ERROR_PAGE_URL))
    print()
