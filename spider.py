#!/usr/bin/env python3
import requests
import re
import sys

read = set()

def load(file):
    return requests.get('http://spacebar.org/f/a/tinyworld/get/{}'.format(file)).text
    # the status code is ALWAYS 200.

def next(name):
    if name == '':return '1'
    edit = list(name)
    for i in range(len(edit)-1, -1, -1):
        if edit[i] in '0123456789':
            if edit[i] == '9':
                edit[i] = '0'
            else:
                edit[i] = chr(ord(edit[i]) + 1)
                break
        else:
            edit.insert(i+1, '1')
            break
    if name[0] == '9' and edit[0] == '0':edit.insert(0, '1')
    return ''.join(edit)

def spider(root):
    if root in read:return
    data = load(root)
    print('spider', root)
    if data.find('404 NOT FOUND') != -1:return
    read.add(root)
    with open('levels/{}.txt'.format(root), 'w') as f:f.write(data)
    spider(next(root))
    for start in (m.start() for m in re.finditer('\\@', data)):
        end = start + 1
        while data[end] in 'abcdefghijklmnopqrstuvwxyz0123456789':
            end += 1
        if data[end] == '.':
            spider(data[start+1:end])
            

spider(sys.argv[1])
