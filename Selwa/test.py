print "hello"
value = 3

alphabet = {'A': [(3, 9), (1.5, -4.5), (-3, 0), (3, 0), (1.5, -4.5)],
            'B': [(0, 9), (4, 0), (2, -1), (0, -2.5), (-2, -1), (-4, 0), (4, 0), (2, -1), (0, -2.5), (-1, -1), (1, 0)],
            'C': [(2, 0), (-2, 1), (0, 7), (2, 1), (4, 0), (-4, 0), (-2, -1), (0, -7), (2, -1), (4, 0)],
            'D': [(0, 9), (4, 0), (2, -3), (0, -3), (-2, -3), (-4, 0), (6, 0)],
            'E': [(0, 9), (6, 0), (-6, 0), (0, -4.5), (6, 0), (-6, 0), (0, -4.5), (6, 0)],
            'F': [(0, 9), (6, 0), (-6, 0), (0, -4.5), (4, 0), (-4, 0), (0, -6.5), (6, 0), (0, 2)],
            'G': [(0, 8), (1, 1), (5, 0), (-5, 0), (-1, -1), (0, -8), (5, 0), (1, 1), (0, 3.5), (-3, 0), (3, 0), (0, -3.5), (-1, -1), (1, 0)],
            'H': [(0, 9), (0, -4.5), (6, 0), (0, 4.5), (0, -9)],
            'I': [(3, 0), (0, 9), (-3, 0), (6, 0), (-3, 0), (0, -9), (3, 0)],
            'J': [(0, 1.5), (0, -1.5), (1, -1), (3, 0), (2, 1), (0, 9), (0, -9)],
            'K': [(0, 9), (0, -4.5), (6, 4.5), (-6, -4.5), (6, -4.5)],
            'L': [(0, 9), (0, -9), (6, 0)],
            'M': [(0, 9), (3, -4.5), (3, 4.5), (0, -9)]}


def printString(cur_x, cur_y, scale, string):
    for letter in string:
        for segment in alphabet[letter]:
            draw(cur_x + segment[0], cur_y + segment[1])
        draw(cur_x + space, cur_y)


def draw(x, y):
    print 'X is now: ' + str(x)
    print 'Y is now: ' + str(y)


printString(0, 0, 1, 'ABC')


JI