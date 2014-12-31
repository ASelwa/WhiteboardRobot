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
HORIZONTAL_SPACE = 1.1
VERT_RES = 0.2
MAX_PIC_SIZE = 100, 100

device = "/dev/ttyACM0"
device2 = "/dev/ttyAMC1"

def main():   
    global cur_x, cur_y, ser

    # Connect to arduino
    try:
        ser = serial.Serial(device, PORT)
        print 'Connected to ', device
    except serial.SerialException:
        ser = serial.Serial(device2, PORT)
        print 'Connected to ', device2
        time.sleep(1)

    # Get the pic
    imagename = 'test.png'
    img = Image.open(imagename).convert('L') # greyscale
    print 'IMAGE SIZE hor_pic_size: ', img.size[0], 'vert_pic_size: ', img.size[1]
    img.thumbnail(MAX_PIC_SIZE, Image.ANTIALIAS)
    hor_pics, vert_pics = img.size
    print 'AFTER SCALING hor_pics: ', hor_pics, 'vert_pics: ', vert_pics

    # User inputs, remember that y is -'ve in my coor system but +'ve in pixel space
    start_x = input('current x position in mm: ')
    start_y = input('current y position in mm: ')
    end_x = input('end x position in mm: ')
    end_y = input('end y position in mm: ')

    # Does the vertical or horizontal dimension determine the picture scale?
    dwg_ratio = vert_pics/float(hor_pics)
    board_ratio = abs( (end_y-start_y) / (end_x-start_x) )
    if dwg_ratio > board_ratio:
        x_dim_max = False
        done_x = int(abs(end_y - start_y) / dwg_ratio)
        done_y = end_y
        print "Y dimension is max"
    else:
        x_dim_max = True
        done_y = int(abs(end_x - start_x) * dwg_ratio)
        done_x = end_x
        print "X dimension is max"

    right = True
    up = False

    del_x = abs(done_x - start_x)
    del_y = abs(done_y - start_y)

    cur_x = start_x
    cur_y = start_y
    cur_x_pix = 0
    cur_y_pix = 0
    prev_x_pix = -1
    prev_y_pix = -1

    # Draw the picture
    while cur_x_pix < hor_pics:
        # get the x, y location in pixel space
        x = int( ( (cur_x - start_x) / float(del_x) ) * hor_pics )
        y = abs(int( ( (cur_y - start_y) / float(del_y) ) * hor_pics ))
        # Need to lookup density value!!

    print "ok, all done"

        
def draw(x,y):
    global cur_x, cur_y, ser
    ser.write(str(int(cur_x))+','+str(int(cur_x+x))+','+
              str(int(cur_y))+','+str(int(cur_y+y))+'\n')
    # Update coordinates
    cur_x, cur_y = cur_x + x, cur_y + y
    dist = math.sqrt( x**2 + y**2 )
    time.sleep( 1.2 * dist/SPEED)

if __name__ == '__main__':
    main()
