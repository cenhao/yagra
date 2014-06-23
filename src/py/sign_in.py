#!/usr/bin/python

''' This is the sign in cgi. '''
from __future__ import print_function
import sys

sys.path.insert(0, '/var/www/yagra/config')

import cgi
import datetime
import json
import os
import hmac
import Cookie
from sys import stderr
import MySQLdb as mdb
from common import ERROR_PAGE_URL, MYSQL_HOST, MYSQL_USER, MYSQL_PWD
from common import HMAC_KEY
from common import HOST_NAME
from common import TEMPLATE_PATH

if ('REQUEST_METHOD' in os.environ and
        os.environ['REQUEST_METHOD'] == 'GET'):
    # If it's a GET request, output sign_in page
    try:
        with open(TEMPLATE_PATH + '/sign_in.html') as fh:
            print('Content-Type: text/html')     # HTML is following
            print()
            print(fh.read(), end='')
    except:
        print('Location: %s' % (ERROR_PAGE_URL))
        print()

    exit(0)

form = cgi.FieldStorage(keep_blank_values=True)
username = form.getfirst('email')
pwd = form.getfirst('pwd')
remember = form.getfirst('remember_me')
response = dict()
cookie = Cookie.SimpleCookie()

print('Content-Type: application/json')     # HTML is following

# Abnormal request
if (username is None) or (pwd is None):
    response['status'] = 'error'
    response['redirect'] = ERROR_PAGE_URL
    print()
    print(json.dumps(response))
    exit(0)

username = mdb.escape_string(username.lower())
pwd = mdb.escape_string(pwd)

try:
    #with mdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PWD) as conn: ??
    conn = mdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PWD, 'db_yagra')
    cursor = conn.cursor()
    print('user = %s' % (pwd, ), file=stderr)
    query = 'SELECT is_actived FROM t_user' +\
            '    WHERE username = %s AND password = %s LIMIT 10'
    cursor.execute(query, (username, pwd))
    rows = cursor.fetchall()

    if len(rows) > 1: # something wrong in the db
        print('Multiple records for user[{0}]'.format(username),
              file=stderr)
        response['status'] = 'error'
        response['redirect'] = ERROR_PAGE_URL
    elif len(rows) == 0: # no such user or wrong password
        response['status'] = 'alert'
        response['message'] = 'Invalid email or password'
    elif rows[0][0] == 0: # The user is not actived
        response['status'] = 'alert'
        response['message'] = 'This email address is not actived'
    else:
        response['status'] = 'ok'
        response['redirect'] = 'http://{0}/yagra/'.format(HOST_NAME)
        cookie['session'] = '{0}|{1}'.format(
                username,
                hmac.new(HMAC_KEY, username+pwd).hexdigest()
        )
        cookie['session']['path'] = '/yagra'
        cookie['session']['httponly'] = 1
        if remember is not None:
            expiration = datetime.datetime.now() + datetime.timedelta(days=90)
            cookie['session']['expires'] = \
                    expiration.strftime('%a, %d-%b-%Y %H:%M:%S %Z')

    # del rows -> how do I perform mysql_free_result here?
    cursor.close()
    conn.close()
except Exception as e:
    print()
    print('Checking user password encounter error: {0}'.format(e),
          file=stderr);
    response['status'] = 'error'
    response['redirect'] = ERROR_PAGE_URL

print(cookie.output())
print()
print(json.dumps(response))
