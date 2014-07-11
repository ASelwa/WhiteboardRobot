#!/usr/bin/env python 

# Whiteboard CNC robot
# Winter 2014
# Badass residents of 83 D'Arcy 

import sys
import serial
import time

PORT = 9600
alphabet = {'A': [(3, 10), (1.5, -5), (-3, 0), (3, 0), (1.5, -5)], 
            'B': [(0, 10), (6, 0), (0, -4), (-3.5, -1), (3.5, -1), (0, -4), (-6, 0), (6, 0)], 
            'C':[(0, 10), (6, 0), (-6, 0), (0, -10), (6, 0)]}
SPACE = 1

# Connect to arduino
device = "/dev/ttyAMC1"

def main():   
    global cur_x, cur_y, ser

    # Starting location
    cur_x = int(sys.argv[1])
    cur_y = -1*int(sys.argv[2])

    # Connect to arduino
    device = "/dev/ttyACM1"
    try:
        ser = serial.Serial(device, PORT)
    except serial.SerialException:
        ser = serial.Serial('/dev/ttyACM0', PORT)
        time.sleep(2)
    finally:
        print 'Connected'

    while(1):
        my_string = raw_input('What u got to say?: ')
        printStringReverse(my_string)

def printStringReverse(string, scale=10):
    for letter in reversed(string):
        for segment in reversed(alphabet[letter]):
            draw(-1 * scale * segment[0], -1 * scale * segment[1])
        draw(-1*SPACE*scale, 0)

def printString(string, scale=10):
    for letter in string:
        for segment in alphabet[letter]:
            draw(scale * segment[0], scale * segment[1])
        draw(SPACE*scale, 0)

def draw(x,y):
    global cur_x, cur_y, ser
    print x, y
    # The A is to verify that a real signal has been sent
    ser.write(str(int(cur_x))+','+str(int(cur_x+x))+','+
              str(int(cur_y))+','+str(int(cur_y+y))+'\n')
    # Update coordinates
    cur_x, cur_y = cur_x + x, cur_y + y
    # Warning if at edge of whiteboard
    if cur_x > 1700 or cur_x < 100 or -1*cur_y > 1400 or -1*cur_y < 200:
        print "WARNING: edge of board at " + str(cur_x) + ',' + str(cur_y)
        sys.exit()
    # Wait for the arduino to finish the line or break after a while
    millis = int(round(time.time() * 1000))
    while(1):
        try:
            waitline = ser.read()
        except: # serial.SerialException:
            print 'Something wrong with serial connection?'
            break
        finally:
            break
        if waitline == 'a':
            break
        current_millis = int(round(time.time() * 1000))
        # Timeout condition
        print current_millis
        if current_millis > millis + 2000:
            print 'Timeout'
            break

if __name__ == '__main__':
    main()
