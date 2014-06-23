#!/usr/bin/python

'''The upload cgi'''

from __future__ import print_function
import sys

sys.path.insert(0, '/var/www/yagra/config')

import Cookie
import os
import hashlib
import cgi
import json
from sys import stderr
import MySQLdb as mdb
from common import MYSQL_HOST, MYSQL_USER, MYSQL_PWD
from common import ERROR_PAGE_URL, HOST_NAME
from common import TEMPLATE_PATH, MAX_IMAGE_SIZE
from common import login_user

if ('REQUEST_METHOD' in os.environ and
        os.environ['REQUEST_METHOD'] == 'GET'):
    try:
        template = ''
        with open(TEMPLATE_PATH + '/upload.html') as fh: template = fh.read()
        username = login_user()
        if username is not None:
            md5 = hashlib.md5(username).hexdigest()
            print('Content-Type: text/html')    # HTML is following
            print()
            print(template % ('/yagra/upload/', username, 
                '<li><a href="/yagra/off.py">Sign out</a></li>', md5))
        else: # not login
            print('Location: /yagra/sign_in/')    # HTML is following
            print()
    except Exception as e:
        print('Something wrong: {0}'.format(e), file=stderr)
        print('Location: %s' % (ERROR_PAGE_URL))
        print()

    exit(0)


print('Content-Type: application/json')
print()

response = dict()

# check if log in
username = login_user()
if username is None:
    response['status'] = 'error'
    response['redirect'] = 'http://%s/sign_in/' % HOST_NAME
    print(json.dumps(response))
    exit(0)

form = cgi.FieldStorage(keep_blank_values=True)
image = None

# get image item
if 'new_image' in form:
    image = form['new_image']
    if isinstance(image, list):
        image = image[0]
    if not image.filename:
        image = None

if image is None:
    response['status'] = 'error'
    response['redirect'] = ERROR_PAGE_URL
else:
    # read only 1MB+10 bytes
    extension = image.filename.split('.')[-1]
    img_data = image.file.read(MAX_IMAGE_SIZE + 16)

    if extension not in ('jpg', 'jpeg', 'png', 'bmp'):
        response['status'] = 'invalid'
        response['message'] = 'Your ' + extension + \
                '%s file type is not supported :('
    elif len(img_data) > MAX_IMAGE_SIZE:
        response['status'] = 'invalid'
        response['message'] = 'Your image is too large.. Sorry :('
    elif image.done == -1:
        response['status'] = 'invalid'
        response['message'] = 'Something wrong happend' + \
                'during image transmition:('
    else:
        md5 = hashlib.md5(username).hexdigest()
        username = mdb.escape_string(username)
        try:
            conn = mdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PWD, 'db_yagra')
            cursor = conn.cursor()
            query = 'INSERT INTO t_avatar ' + \
                    'VALUES(%s, %s, NOW(), %s, %s, 0, NULL) ' + \
                    'ON DUPLICATE KEY ' + \
                    'UPDATE update_time=(NOW()), avatar=(%s)'
            cursor.execute(query,
                    (md5, username, img_data, extension, img_data))
            cursor.close()
            conn.commit()
            conn.close()
        except Exception as e:
            cursor.close()
            conn.close()
            print('Insert image into database fails: %s' % (e), file=stderr)
            response['status'] = 'error'
            response['redirect'] = ERROR_PAGE_URL
            print(json.dumps(response))
            exit(0)

        response['status'] = 'ok'
        response['api'] = md5

print(json.dumps(response))
