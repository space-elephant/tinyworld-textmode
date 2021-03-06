#!/usr/bin/env python3
import sys
import display
import curses
from rules import search, convert
import requests

net = '-i' in sys.argv or '--net' in sys.argv

def load(name):
    if net:
        data = requests.get('http://spacebar.org/f/a/tinyworld/get/{}'.format(name)).text
    else:
        try:
            with open('levels/{}.txt'.format(name)) as f:data = f.read()
        except FileNotFoundError:
            with open('404.txt') as f:data = f.read()
    return [list(x) for x in display.display(data)]

copycolor = '-g' in sys.argv

def draw(data, player, screen):
    #print('draw', sys.stderr)
    for y in range(len(data)):
        for x in range(len(data[y])):
            #print(y, x, sys.stderr)
            point = data[y][x]
            if point == ' ':
                if player == [x, y]:
                    #print(y, x, repr('T'), sys.stderr)
                    try:
                        if copycolor:
                            screen.addstr(y, x, 'T',
                                          curses.color_pair(red))
                        else:
                            screen.addstr(y, x, 'T', curses.color_pair(onspace))
                    except curses.error:pass
            elif point == 'Y' and not copycolor:
                try:screen.addstr(y, x, 'Y', curses.color_pair(onspace))
                except curses.error:pass
            else:
                if copycolor:
                    try:pair = colors[point]
                    except KeyError:pair = (white, 0)
                    color = pair[0]
                    flag = pair[1]
                    try:
                        if player == [x, y]:
                            screen.addstr(y, x, 'T',
                                          curses.color_pair(red))
                        else:screen.addstr(y, x, data[y][x],
                                           curses.color_pair(color) | flag)
                    except curses.error:pass
                else:
                    if point in nonsolid:color = soft
                    elif point in deadly:color = death
                    else:color = wall
                    if player == [x, y]:color += onspace
                    #print(y, x, repr(data[y][x]), sys.stderr)
                    try:screen.addstr(y, x, data[y][x],
                                      curses.color_pair(color))
                    except curses.error:pass
    sys.stdout.flush()

print('T in Y World by Tom VII for Ludum Dare 23.')
print()

    
if '-y' in sys.argv:start = 'y'
elif '-n' in sys.argv:start = 'n'
elif '-e' in sys.argv:start = ''
else:start = input('Play (Y/n) ')

if start == '':
    first = 'tutorial8'
elif start == 'n' or start == 'N':
    first = 'tutorial0'
elif start == 'y' or start == 'Y':
    first = 'tutorial1'
else:
    first = start

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
    try:point = level[player[1]][player[0]]
    except IndexError:return undo
    if point in nonsolid:return go
    if point in deadly:return restart
    return undo

green = 1
blue = 2
cyan = 3
red = 4
yellow = 5
white = 6
magenta = 7

onspace = green
death = red
ondeath = yellow
soft = blue
onsoft = cyan
wall = white
onwall = magenta

colors = {
    'A': (blue, 0),
    'B': (cyan, 0),
    'C': (blue, 0),
    'D': (blue, 0),
    'E': (cyan, 0),
    'F': (cyan, 0),
    'G': (green, 0),
    'H': (yellow, 0),
    'I': (blue, 0),
    'J': (red, 0),
    'K': (magenta, 0),
    'L': (magenta, curses.A_DIM),
    'M': (blue, 0),
    'N': (white, curses.A_DIM),
    'O': (green, 0),
    'P': (magenta, curses.A_DIM),
    'Q': (red, curses.A_DIM),
    'R': (yellow, 0),
    'S': (yellow, curses.A_DIM),
    'T': (red, curses.A_DIM),
    'U': (yellow, 0),
    'V': (red, 0),
    'W': (yellow, 0),
    'X': (magenta, 0),
    'Y': (yellow, 0),
    'Z': (magenta, curses.A_DIM),
    '=': (yellow, 0),
    '\\':(magenta, 0),
    '/': (blue, 0),
    "'": (cyan, 0),
    ',': (cyan, 0),
    '~': (yellow, 0),
    '!': (red, 0),
    '@': (red, 0),
    '#': (white, curses.A_DIM),
    '+': (white, curses.A_DIM),
    '$': (cyan, 0),
    '%': (green, 0),
    '^': (green, 0),
    '&': (green, curses.A_DIM),
    '*': (yellow, 0),
    '?': (yellow, 0),
}

def main(screen):
    curses.curs_set(False)
    curses.init_pair(red, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(yellow, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(blue, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(cyan, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(white, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(magenta, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(green, curses.COLOR_GREEN, curses.COLOR_BLACK)
    name = first
    player = None
    while True:
        level = load(name)
        found = False
        for line in range(len(level)-1, -1, -1):
            for tile in range(len(level[line])-1, -1, -1):
                if level[line][tile] == 'T':
                    player = [tile, line]
                    found = True
                    break
            if found:break
        with open('log.txt', 'w') as f:f.write('{} {}\n'.format(len(level), player))
        while level[player[1]][player[0]] != 'Y':
            screen.clear()
            draw(level, player, screen)
            screen.refresh()
            oldplayer = list(player)
            command = screen.getch()
            char = False
            if command == ord('w') or command == curses.KEY_UP:
                player[1] -= 1
                char = True
            elif command == ord('s') or command == curses.KEY_DOWN:
                player[1] += 1
                char = True
            elif command == ord('a') or command == curses.KEY_LEFT:
                player[0] -= 1
                char = True
            elif command == ord('d') or command == curses.KEY_RIGHT:
                player[0] += 1
                char = True
            elif command == ord('r'):break # restart
            elif command == ord('e') or command == ord('q'):exit()
            now = valid(level, player)
            if now == undo:player = oldplayer
            elif now == restart:break
            if char:
                data = search(level, player)
                if data[0] == convert['@']:
                    name = data[1]
                    break

        if level[player[1]][player[0]] == 'Y':
            name = next(name)

curses.wrapper(main)
