#!/usr/bin/env python
# encoding: utf-8

from boto.s3.connection import S3Connection
from secrets import *
from sys import argv
from urlparse import urlparse
from urllib import unquote

if __name__ == "__main__":
    o = urlparse(argv[1])
    conn = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY, debug=0)
    bucket = conn.create_bucket(o.hostname.split('.')[0])
    key_name = unquote(o.path[1:])
    key = bucket.get_key(key_name)
    for k,v in key.metadata.iteritems():
        print '%s: %s' % (k, unquote(v))
