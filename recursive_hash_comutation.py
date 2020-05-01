#!/usr/bin/env python
import os
import os.path as os_path
import logging
import hashlib

def file_hash(filepath):
    blocksize = 64*1024
    sha = hashlib.sha256()
    with open(filepath, 'rb') as fp:
        while True:
            data = fp.read(blocksize)
            if not data:
                break
            sha.update(data)
    return sha.hexdigest() 

ROOT = "c:\\Users\\aniruddha\\Downloads"
for root, dirs, files in os.walk(ROOT):
    for file_path in [os_path.join(root,f) for f in files]:
        size = os_path.getsize(file_path)
        sha = file_hash(file_path)
        name = os_path.relpath(file_path, ROOT)
        print("%s,%s,%s"%(size,sha,name))
