#!/usr/bin/env python3
from math import copysign
def sign(x):
    return copysign(1, x) if x else 0

right = 0
up = 1
left = 2
down = 3
toT = 4
fromT = 5
replace = 6
warp = 7
music = 8
end = 9

convert = {
    '>': right,
    '^': up,
    '<': left,
    'v': down,
    '(': toT,
    ')': fromT,
    '=': replace,
    '@': warp,
    'm': music,
    '.': end,
}

class rule:
    def __init__(self, string):
        self.valid = True
        self.start = string[0]
        self.data = []
        index = 1
        while True:
            try:
                if convert[string[index]] >= replace:break
            except KeyError:
                self.valid = False
                return
            self.data.append(convert[string[index]])
            self.data.append(string[index+1])
            index += 2
        self.mode = convert[string[index]]
        if self.mode == end:
            self.valid = False
            return
        self.newstart = None
        self.result = []
        if self.mode == replace:
            self.newstart = string[index+1]
            while True:
                index += 2
                try:
                    if string[index] == '.':break
                except IndexError:
                    self.valid = False
                    return
                try:self.result.append(convert[string[index]])
                except KeyError:
                    self.valid = False
                    return
                self.result.append(string[index+1])
            self.end = index
        else:
            while True:
                index += 1
                try:
                    if string[index] == '.':break
                except IndexError:
                    self.valid = False
                    return
                self.result.append(string[index])
            self.end = index
    def match(self, level, player, marked):
        if not self.valid:return
        for y in range(len(level)):
            for x in range(len(level[y])):
                try:
                    playerrelative = (x - player[0], y - player[1])
                    loc7, loc6 = 0, 0
                    if abs(playerrelative[0]) >= abs(playerrelative[1]):
                        loc7 = int(sign(playerrelative[0]))
                    else:
                        loc6 = int(sign(playerrelative[1]))

                    if not marked[y][x] and level[y][x] == self.start:
                        testx = x
                        testy = y
                        found = True
                        for test in range(0, len(self.data), 2):
                            direction = self.data[test]
                            if direction == right:testx += 1
                            elif direction == left:testx -= 1
                            elif direction == down:testy += 1
                            elif direction == up:testy -= 1
                            elif direction == fromT:
                                testx += loc7
                                testy += loc6
                            elif direction == toT:
                                testx -= loc7
                                testy -= loc6
                            if marked[testy][testx] or level[testy][testx] != self.data[test+1]:
                                found = False
                                break
                        if found:
                            if self.mode == replace:
                                marked[y][x] = True
                                level[y][x] = self.newstart
                                setx = x
                                sety = y
                                for point in range(0, len(self.result), 2):
                                    direction = self.result[point]
                                    if direction == right:setx += 1
                                    elif direction == left:setx -= 1
                                    elif direction == down:sety += 1
                                    elif direction == up:sety -= 1
                                    elif direction == fromT:
                                        setx += loc7
                                        sety += loc6
                                    elif direction == toT:
                                        setx -= loc7
                                        sety -= loc6
                                    level[sety][setx] = self.result[point+1]
                                    marked[sety][setx] = True
                            else:return (self.mode, self.result) # warp
                except IndexError:pass
                                
def search(level, player):
    back = level[player[1]][player[0]]
    level[player[1]][player[0]] = 'T'
    sound = None
    rules = []
    marked = []
    for y in range(len(level)):
        marked.append([])
        for x in range(len(level[y])):
            marked[-1].append(False)
            if level[y][x] == '?':
                rules.append(rule(''.join(level[y][x+1:])))
    for point in rules:
        test = point.match(level, player, marked)
        if test != None:
            if test[0] == warp:
                return (warp, ''.join(test[1]))
            else:
                sound = test[1]
    level[player[1]][player[0]] = back
    return (music, sound)

if __name__ == '__main__':
    level = [list(x) for x in [
        '###############',
        '#?T>B> =T> >B.#',
        '###############',
        '#   TB        #',
        '###############',
    ]]
    #search(level, (0, 0))
    test = rule('T>B> =T> >B.')
    marked = [[False] * len(level[0]) for i in range(len(level))]
    player = (0, 0)
    test.match(level, player, marked)
    for line in level:print(''.join(line))
