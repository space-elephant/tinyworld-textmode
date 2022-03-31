#!/usr/bin/env python3
def sign(x):
    if x < 0:return -1
    if x > 0:return 1
    return 0

right = '>'
up = '^'
left = '<'
down = 'v'
toT = '('
fromT = ')'
replace = '='
warp = '@'
music = 'm'
end = '.'
forward = ']'
backward = '['
turnleft = '{'
turnright = '}'
any = 'a'
remote = 'r'
matchT = 't'

class rule:
    def __init__(self, string, warps):
        self.valid = True
        self.start = string[0]
        self.data = []
        index = 1
        while True:
            try:
                if string[index] in (replace, warp, music):break
            except (KeyError, IndexError):
                self.valid = False
                return
            self.data.append(string[index])
            self.data.append(string[index+1])
            index += 2
        self.mode = string[index]
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
                try:self.result.append(string[index])
                except KeyError:
                    self.valid = False
                    return
                try:self.result.append(string[index+1])
                except IndexError:
                    self.valid = False
                    return
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
        if self.mode == warp:warps.add(''.join(self.result))
    def match(self, level, player, marked):
        if not self.valid:return
        for y in range(len(level)):
            for x in range(len(level[y])):
                playerrelative = (x - player[0], y - player[1])
                directionx, directiony = 0, 0
                if abs(playerrelative[0]) >= abs(playerrelative[1]):
                    directionx = int(sign(playerrelative[0]))
                else:
                    directiony = int(sign(playerrelative[1]))

                if not marked[y][x] and level[y][x] == self.start:
                    testx = x
                    testy = y
                    found = True
                    for test in range(0, len(self.data), 2):
                        strict = True
                        direction = self.data[test]
                        object = self.data[test+1]
                        if direction == any:
                            strict = False
                            direction = self.data[test+1]
                        elif direction == matchT:
                            direction = self.data[test+1]
                            object = ''
                        if direction == right:testx += 1
                        elif direction == left:testx -= 1
                        elif direction == down:testy += 1
                        elif direction == up:testy -= 1
                        elif direction == fromT:
                            testx += directionx
                            testy += directiony
                        elif direction == toT:
                            testx -= directionx
                            testy -= directiony
                        try:
                            if strict and (marked[testy][testx] or (level[testy][testx] != object and not(object == '' and testx == player[0] and testy == player[1]))):
                                found = False
                                break
                        except IndexError:
                            found = False
                            break
                    if found:
                        if self.mode == replace:
                            marked[y][x] = True
                            level[y][x] = self.newstart
                            setx = x
                            sety = y
                            print(self.result)
                            for point in range(0, len(self.result), 2):
                                direction = self.result[point]
                                object = self.result[point+1]
                                strict = True
                                print(object, direction)
                                if direction == any:
                                    strict = False
                                    direction = self.data[point+1]
                                elif direction == matchT:
                                    direction = object
                                    object = ''
                                print(object, direction)
                                if direction == right:setx += 1
                                elif direction == left:setx -= 1
                                elif direction == down:sety += 1
                                elif direction == up:sety -= 1
                                elif direction == fromT:
                                    setx += directionx
                                    sety += directiony
                                elif direction == toT:
                                    setx -= directionx
                                    sety -= directiony
                                if strict:
                                    if object == '':
                                        if setx >= 0 and sety >= 0 and setx < 40 and sety < 25:
                                            player[0] = setx
                                            player[1] = sety
                                            marked[sety][setx] = True
                                        else:return
                                    else:
                                        if setx >= 0 and sety >= 0 and setx < 40 and sety < 25:
                                            level[sety][setx] = object
                                            marked[sety][setx] = True
                                        else:return
                        else:return (self.mode, self.result) # warp

def expandremote(string, warps):
    remotes = []
    convert = None
    for i in range(1, len(string), 2):
        if string[i] == remote:remotes.append(i)
        elif string[i] in (replace, warp, music):
            convert = i
            if string[i] != replace:break
    if convert == None:return ()
    first = []
    second = []
    for point in remotes:
        if point < convert:first.append(point)
        else:second.append(point)
    if len(first) == 0:
        edit = list(string)
        second.reverse()
        for x in second:
            edit.pop(x)
            edit.pop(x)
        return rule(''.join(edit), warps),
    else:
        rules = []
        remotes.reverse()
        for length in range(40):
            edit = list(string)
            for point in remotes:
                type = any + edit[point+1]
                edit.pop(point)
                edit.pop(point)
                for _ in range(length):
                    edit.insert(point, type)
            if len(''.join(edit)) > 160:break
            rules.append(rule(''.join(edit), warps))
        return rules

def makerule(string, warps):
    fore = []
    back = []
    leftt = []
    rightt = []
    for i in range(1, len(string), 2):
        if string[i] in (any, remote, matchT):
            if string[i+1] == forward:fore.append(i+1)
            elif string[i+1] == backward:back.append(i+1)
            elif string[i+1] == turnleft:leftt.append(i+1)
            elif string[i+1] == turnright:rightt.append(i+1)
        elif string[i] == forward:fore.append(i)
        elif string[i] == backward:back.append(i)
        elif string[i] == turnleft:leftt.append(i)
        elif string[i] == turnright:rightt.append(i)
        elif string[i] in (warp, music):break
    if len(fore) > 0 or len(back) > 0 or len(leftt) > 0 or len(rightt) > 0:
        rules = []
        edit = list(string)
        for type in range(4):
            main = (right, up, left, down)[type]
            reverse = (left, down, right, up)[type]
            rleft = (up, left, down, right)[type]
            rright = (down, right, up, left)[type]
            for i in fore:edit[i] = main
            for i in back:edit[i] = reverse
            for i in leftt:edit[i] = rleft
            for i in rightt:edit[i] = rright
            rules.extend(expandremote(''.join(edit), warps))
        return rules
    else:return expandremote(string, warps)
    
def search(level, player):
    warps = set()
    back = level[player[1]][player[0]]
    level[player[1]][player[0]] = 'T'
    playerx = player[1]
    playery = player[0]
    sound = None
    rules = []
    marked = []
    for y in range(len(level)):
        marked.append([])
        for x in range(len(level[y])):
            marked[-1].append(False)
            if level[y][x] == '?':
                rules.extend(makerule(''.join(level[y][x+1:]), warps))
    for point in rules:
        test = point.match(level, player, marked)
        if test != None:
            if test[0] == warp:
                return (warp, ''.join(test[1]))
            else:
                sound = test[1]
    level[playerx][playery] = back
    return (music, sound, warps)

if __name__ == '__main__':
    level = [list(x) for x in [
        '###################',
        '#                 #',
        '#  ####           #',
        '#                 #',
        '###################',
    ]]
    #search(level, (0, 0))
    rule = rule('#tv=#t^.', [])
    marked = [[False] * len(level[0]) for i in range(len(level))]
    player = [4, 3]    
    #for rule in rules:
    rule.match(level, player, marked)
    level[player[1]][player[0]] = 'T'
    for line in level:print(''.join(line))
