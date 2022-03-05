#!/usr/bin/env python3
import requests

read = set()

def load(file):
    return requests.get('http://spacebar.org/f/a/tinyworld/get/{}'.format(file)).text
    # the status code is ALWAYS 200.

levels = []
index = 0
done = False
while not done:
    print('map page {}'.format(index))
    map = load('all{}'.format(index))
    for pos in range(210, 930, 40):
        if map[pos-1] == '@':
            name = []
            while map[pos + len(name)] != '.':
                name.append(map[pos + len(name)])
            levels.append(''.join(name))
        else:done = True
    index += 1

with open('levels.txt', 'w') as f:f.write('\n'.join(levels) + '\n')
print(levels)
