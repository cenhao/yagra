#!/usr/bin/python

'''The api cgi.'''

from __future__ import print_function
import sys
sys.path.insert(0, '/var/www/yagra/config')
import cgi
from sys import stderr
import MySQLdb as mdb
from common import MYSQL_HOST, MYSQL_USER, MYSQL_PWD

form = cgi.FieldStorage(keep_blank_values=True)
md5 = form.getfirst('key', None)

if md5 is not None:
    try:
        conn = mdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PWD, 'db_yagra')
        cursor = conn.cursor()
        query = 'SELECT avatar, file_type FROM t_avatar ' + \
                '   WHERE user_md5 = %s'
        cursor.execute(query, (mdb.escape_string(md5), ))
        rows = cursor.fetchall()

        if len(rows) != 0:
            print('Content-Type: Image/{0}'.format(rows[0][1]))
            print()
            print(rows[0][0])
            exit(0)
    except Exception as e:
        print('Api error: {0}'.format(e), file=stderr)

print('here', file=stderr)

print("Content-Type: Image/png")
print()
print(file('/var/www/html/img/default.png', 'r').read())
