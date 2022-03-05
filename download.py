#!/usr/bin/env python3
import requests

def load(file):
    return requests.get('http://spacebar.org/f/a/tinyworld/get/{}'.format(file)).text

with open('levels.txt') as f:
    for level in f.readlines():
        level = level[:-1]
        print(level)
        with open('levels/{}.txt'.format(level), 'w') as g:
            g.write(load(level))
