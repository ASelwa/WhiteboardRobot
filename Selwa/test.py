alphabet = {'A': [(3, 10), (1.5, -5), (-3, 0), (3, 0), (1.5, -5)], 
            'B': [(0, 10), (6, 0), (0, -4), (-3.5, -1), (3.5, -1), (0, -4), (-6, 0), (6, 0)], 
            'C':[(0, 10), (6, 0), (-6, 0), (0, -10), (6, 0)]}


def printString(cur_x, cur_y, scale, string):
    for letter in string:
        for segment in alphabet[letter]:
            draw(cur_x + segment[0], cur_y + segment[1])
        draw(cur_x + space, cur_y)


def draw(x, y):
    print 'X is now: ' + str(x)
    print 'Y is now: ' + str(y)


printString(0, 0, 1, 'ABC')


