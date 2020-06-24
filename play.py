#!/usr/bin/env python3
import sys
import display
import readchar

net = '-n' in sys.argv or '--net' in sys.argv

def load(name):
    if net:raise TypeError('net is not yet supported')
    else:
        with open('levels/{}.txt'.format(name)) as f:data = f.read()
        return [list(x) for x in display.display(data)]

def draw(data):
    for x in data:print(''.join(x))

if '-y' in sys.argv:start = 'y'
elif '-n' in sys.argv:start = 'n'
elif '-e' in sys.argv:start = ''
else:start = input('Play (Y/n) ')

if start == '':
    name = 'tutorial8'
elif start[0] == 'n' or start[0] == 'N':
    name = 'tutorial0'
else:
    name = 'tutorial1'

nonsolid = set(' AEIOY')
deadly = set('PQRSTUVWXZ')

go = 0
undo = 1
restart = 2

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

def valid(level, player):
    point = level[player[0]][player[1]]
    if point in nonsolid:return go
    if point in deadly:return restart
    return undo

while True:
    level = load(name)
    player = None
    for line in range(len(level)-1, -1, -1):
        for tile in range(len(level[line])-1, -1, -1):
            if level[line][tile] == 'T':
                player = [line, tile]
                break
        if player != None:break
        
    while level[player[0]][player[1]] != 'Y':
        level[player[0]].insert(player[1], "\u0304")#032A
        draw(level)
        level[player[0]].pop(player[1])
        command = readchar.readchar()
        oldplayer = list(player)
        if command == 'w':player[0] -= 1
        elif command == 's':player[0] += 1
        elif command == 'a':player[1] -= 1
        elif command == 'd':player[1] += 1
        elif command == 'r':break # restart
        elif command == 'e':exit()
        now = valid(level, player)
        if now == undo:player = oldplayer
        elif now == restart:break
        
    if level[player[0]][player[1]] == 'Y':
        name = next(name)
