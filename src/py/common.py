#!/usr/bin/python

''' This is a python module for common functions and constants. '''
from __future__ import print_function
import os
import Cookie
import hmac
from sys import stderr
import MySQLdb as mdb

MYSQL_HOST = 'localhost'
MYSQL_USER = 'yagra_admin'
MYSQL_PWD = 'scriptyagar123'
''' Above are for the mysql connection '''

HMAC_KEY = 'yagra_key'
''' session hash key '''

TEMPLATE_PATH = '/var/www/html/templates'

HOST_NAME = 'cenhao.chinacloudapp.cn'

ERROR_PAGE_URL = 'http://' + HOST_NAME + '/error.html'
''' Page to show when unexcepted error occurs. '''

MAX_IMAGE_SIZE = 1 * 1024 * 1024 # 1 MB

def _get_username_from_session(session):
    ''' Test if the session is valid, return username or None. '''
    session_list = session.split('|')
    if (len(session_list) != 2): return None
    username = mdb.escape_string(session_list[0].lower())
    digest = session_list[1]
    ret = None
    rows = None

    try:
        conn = mdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PWD, 'db_yagra')
        cursor = conn.cursor()
        query = 'SELECT password FROM t_user' + \
                '   WHERE username = "{0}" AND is_actived > 0 LIMIT 10'
        query = query.format(username)
        cursor.execute(query)
        rows = cursor.fetchall()

        if len(rows) > 1: # something wrong in the db
            print('Multiple records for user[{0}]'.format(username),
                    file=stderr)
            raise StandardError('Database data error.')
        elif len(rows) == 1:
            pwd = rows[0][0]
            if (digest == hmac.new(HMAC_KEY, username+pwd).hexdigest()):
                ret = username
    except Exception as e:
        del rows
        cursor.close()
        conn.close()
        raise e

    del rows
    cursor.close()
    conn.close()
    return ret

def login_user():
    if 'HTTP_COOKIE' in os.environ:
        cookie = Cookie.SimpleCookie(os.environ['HTTP_COOKIE'])
        session = cookie['session'].value
        username = _get_username_from_session(session)
        if username is not None:
            return username
    return None
