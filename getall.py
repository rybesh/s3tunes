#!/usr/bin/env python
# encoding: utf-8

from boto.s3.connection import S3Connection
from boto.s3.key import Key
from urllib import quote
from secrets import *

conn = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY, debug=0)
bucket = conn.create_bucket(BUCKET)
m3u = open('everything.m3u', 'a')
for key in bucket.list():
    m3u.write('http://%s.s3.amazonaws.com/%s\n' 
              % (key.bucket.name, quote(key.name)))
m3u.close()
