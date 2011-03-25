#!/usr/bin/env python
# encoding: utf-8

from sys import argv, stdout
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from urllib import urlretrieve, quote
from random import shuffle
import os

from secrets import *

ITUNES = '/Volumes/Media/iTunes/iTunes Media/Music/'
DOWNLOADS = '/Volumes/Media/Downloads/'
TARGET_SIZE = 21474836480

def progress(blocks, blocksize, total):
    downloaded = blocks * blocksize
    length = 72
    fraction = float(downloaded) / total
    bar = (int(length * fraction) * '=').ljust(length)
    percent = ('%s%%' % int(fraction * 100)).rjust(5)
    progress = '[%s]%s' % (bar, percent)
    stdout.write('\x1B[2K') # erase current line
    stdout.write('\x1B[0G') # move to column 0
    stdout.write(progress)
    stdout.flush()

conn = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY, debug=0)
bucket = conn.create_bucket(BUCKET)

# First, make sure we have local copies of all files.
total_size = 0
keys = []
for key in bucket.list():
    keys.append(key)
    total_size += key.size
    def exists_in(location):
        path = location + key.name
        return (os.path.exists(path) and 
                os.path.getsize(path) == key.size)
    if exists_in(ITUNES) or exists_in(DOWNLOADS):
        continue
    folder, filename = key.name.rsplit('/', 1)
    print '\nDownloading %s ...' % filename
    url = 'http://%s.s3.amazonaws.com/%s\n' % (key.bucket.name, quote(key.name))
    if not os.path.exists(DOWNLOADS + folder):
        os.makedirs(DOWNLOADS + folder)
    urlretrieve(url, DOWNLOADS + key.name, progress)

# Then, start pruning.
shuffle(keys)
count = 0
for key in keys:
    if total_size <= TARGET_SIZE:
        break
    total_size -= key.size
    key.delete()
    count += 1

print '\nDeleted %s files.' % count
print 'Total size is now: %s' % total_size
    
