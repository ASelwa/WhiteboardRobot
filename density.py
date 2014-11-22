#!/usr/bin/env python 

# Whiteboard CNC robot
# Winter 2014
# Badass residents of 83 D'Arcy 

import sys
import serial
import time
import subprocess
import math
from PIL import Image

SPEED = 30 # mm/s
PORT = 9600
SPACE = 2
LEFT_EDGE = 100
RIGHT_EDGE = 1800
TOP_EDGE = 100
BOTTOM_EDGE = 1000

device = "/dev/ttyACM0"
device2 = "/dev/ttyAMC1"

def main():   
    global cur_x, cur_y, scale, ser

    # Connect to arduino
    try:
        ser = serial.Serial(device, PORT)
        print 'Connected to ', device
    except serial.SerialException:
        ser = serial.Serial(device2, PORT)
        print 'Connected to ', device2
        time.sleep(1)

    # Get the pic
    imagename = 'testimg.png'
    img = Image.open(imagename).convert('L') # greyscale
    print 'IMAGE SIZE hor_size: ', img.size[0], 'vert_size: ', img.size[1]
    max_size = 100, 100 # TODO change this
    img.thumbnail(max_size, Image.ANTIALIAS)
    hor_size, vert_size = img.size
    print 'AFTER SCALING hor_size: ', hor_size, 'vert_size: ', vert_size

    # User inputs
    cur_x = input('current x position in mm: ')
    cur_y = -1*input('current y position in mm: ')
    end_x = input('end x position in mm: ')
    end_y = -1*input('end y position in mm: ')
    res = input('resolution in mm: ')

    # These are the values which match up with hor_size, vert_size
    x, y = 0, 0
    up = True
    while x < hor_size:
        if up == True:
            print 'going up'
            while y < vert_size:
                print x, y
                # pixel density between 0 and 1
                density = img.getpixel((x, vert_size - 1 - int(y)))/255
                print 'den: ', density
                max_len = (1 - density) * scale
                if max_len < 0.5:
                    len = 0.5
                print 'len: ', len
                if y * len > vert_size:
                    len = vert_size - y - 1
                    if len == 0:
                        break

                draw(2*scale,0)
                draw(0,scale*len/2.0)
                draw(-2*scale,0)
                draw(0,scale*len/2.0)

                y += len
            draw(scale*2.2,0)
            x += 2.2
            print 'moving over'
            print 'x, y: ', x, y
        else:
            print 'going down'
            while y > 0:
                print x, y
                density = img.getpixel((x, vert_size - 1 - int(y)))/300.0 + 0.1 # 0.1 so that it does move sometimes. 0 < density < 1
                print 'den: ', density
                len = (1 - density) * 7
                if len < 0.5:
                    len = 0.5
                print 'len: ', len
                if y - len < 0:
                    len = y
                    if len == 0:
                        break

                draw(2*scale,0)
                draw(0,-scale*len/2.0)
                draw(-scale*2,0)
                draw(0,-scale*len/2.0)

                y -= len
            draw(scale*2.2,0)
            x += 2.2
            print 'moving over'
        up = not up

def draw(x,y):
    global cur_x, cur_y, ser
    #print '(', x, y, ')',
    # The A is to verify that a real signal has been sent
    ser.write(str(int(cur_x))+','+str(int(cur_x+x))+','+
              str(int(cur_y))+','+str(int(cur_y+y))+'\n')
    # Update coordinates
    cur_x, cur_y = cur_x + x, cur_y + y
    # Warning if at edge of whiteboard
    if cur_x > RIGHT_EDGE or cur_x < LEFT_EDGE or -1*cur_y > BOTTOM_EDGE or -1*cur_y < TOP_EDGE:
        print "WARNING: edge of board at " + str(cur_x) + ',' + str(cur_y)
        sys.exit()
    # Wait for the arduino to finish the line or break after a while
    dist = math.sqrt( x**2 + y**2 )
    time.sleep(1.2*dist/SPEED)
    

if __name__ == '__main__':
    main()
