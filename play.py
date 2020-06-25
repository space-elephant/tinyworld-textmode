#!/usr/bin/env python3
import sys
import display
import curses
from rules import search, convert

net = '-i' in sys.argv or '--net' in sys.argv

def load(name):
    if net:raise TypeError('net is not yet supported')
    else:
        with open('levels/{}.txt'.format(name)) as f:data = f.read()
        return [list(x) for x in display.display(data)]

def draw(data, player, screen):
    #print('draw', sys.stderr)
    for y in range(len(data)):
        for x in range(len(data[y])):
            #print(y, x, sys.stderr)
            point = data[y][x]
            if point == ' ':
                if player == [x, y]:
                    #print(y, x, repr('T'), sys.stderr)
                    try:screen.addstr(y, x, 'T', curses.color_pair(onspace))
                    except curses.error:pass
            elif point == 'Y':
                try:screen.addstr(y, x, 'Y', curses.color_pair(onspace))
                except curses.error:pass
            else:
                if point in nonsolid:color = soft
                elif point in deadly:color = death
                else:color = wall
                if player == [x, y]:color += onspace
                #print(y, x, repr(data[y][x]), sys.stderr)
                try:screen.addstr(y, x, data[y][x], curses.color_pair(color))
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
elif start[0] == 'n' or start[0] == 'N':
    first = 'tutorial0'
else:
    first = 'tutorial1'

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
    point = level[player[1]][player[0]]
    if point in nonsolid:return go
    if point in deadly:return restart
    return undo

onspace = 1
death = 2
ondeath = 3
soft = 4
onsoft = 5
wall = 6
onwall = 7

def main(screen):
    curses.curs_set(False)
    curses.init_pair(death, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(ondeath, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(soft, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(onsoft, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(wall, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(onwall, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(onspace, curses.COLOR_GREEN, curses.COLOR_BLACK)
    name = first
    while True:
        level = load(name)
        player = None
        for line in range(len(level)-1, -1, -1):
            for tile in range(len(level[line])-1, -1, -1):
                if level[line][tile] == 'T':
                    player = [tile, line]
                    break
            if player != None:break

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
