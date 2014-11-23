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
    imagename = 'testimg.png'
    img = Image.open(imagename).convert('L') # greyscale
    print 'IMAGE SIZE hor_pic_size: ', img.size[0], 'vert_pic_size: ', img.size[1]
    max_pic_size = 100, 100
    img.thumbnail(max_pic_size, Image.ANTIALIAS)
    hor_pic_size, vert_pic_size = img.size
    print 'AFTER SCALING hor_pic_size: ', hor_pic_size, 'vert_pic_size: ', vert_pic_size

    # User inputs, remember that y is -'ve in my coor system but +'ve in pixel space
    start_x = input('current x position in mm: ')
    start_y = -1*input('current y position in mm: ')
    end_x = input('end x position in mm: ')
    end_y = -1*input('end y position in mm: ')
    res = input('resolution in mm: ')

    # Does the vertical or horizontal dimension determine the picture scale?
    dwg_ratio = vert_pic_size/hor_pic_size
    board_ratio = abs( (end_y-start_y) / (end_x-start_x) )
    if dwg_ratio > board_ratio:
        x_dim_max = False
        far_x = int(abs(end_y - start_y) / dwg_ratio)
        top_y = end_y
        print "Y dimension is max"
    else:
        x_dim_max = True
        top_y = int((end_x - start_x) * dwg_ratio)
        far_x = end_x
        print "X dimension is max"

    right = True
    up = True

    cur_x = start_x
    cur_y = start_y

    # Draw the picture
    while cur_x < end_x:
        # get the x, y location in pixel space
        if x_dim_max:
            x = int( ( (cur_x - start_x) / (end_x - start_x) ) * hor_pic_size )
            x = max( min( x, far_x ), 0)
            y = int( abs( ( (cur_y - start_y) / (top_y - start_y) ) * vert_pic_size) )
            y = max( min( abs(y), top_y ), 0)
        else:
            y = int( abs( ( (cur_y - start_y) / (end_y - start_y) ) * vert_pic_size) )
            y = max( min( abs(y), top_y ), 0)
            x = int( ( (cur_x - start_x) / (far_x - start_x) ) * hor_pic_size )
            x = max( min( x, far_x ), 0)
        print "at x,y: ", x, y

        # Find an assigned length based on the current location
        # pixel density between 0 and 1
        density = img.getpixel( (x, vert_pic_size - 1 - y) ) / 255
        print "density: ", density
        assigned_length = (1-density) * res
        print "first assigned length: ", assigned_length

        # Average values over the length of the assigned length
        # what is the index of the y pixel at the end of the assigned length?
        if up:
            last_y = int( abs( ( (cur_y + assigned_length - start_y) / (top_y - start_y) ) * vert_pic_size) )
        else:
            last_y = int( abs( ( (cur_y - assigned_length - start_y) / (top_y - start_y) ) * vert_pic_size) )
        last_y = max( min( abs(y), vert_pic_size ), 0)
        print "first last y: ", last_y
        sum = 0
        for y_index in range( min(y,last_y), max(y,last_y) ):
            print y_index
            sum += img.getpixel( (x, vert_pic_size - 1 - y) ) / 255
        if last_y != y:
            avg = sum / abs(y - last_y)
        else:
            avg = density
        print "average density: ", avg
        assigned_length = (1-avg) * res
        print "next assigned_length: ", assigned_length

        # Check to see if the derivative exceeds a certain threshold and stop there
        # TODO

        # Minimum line length
        assigned_length = max( assigned_length, res * VERT_RES )
        print "final assigned length: ", assigned_length

        # The maximum length is the edge of the drawing area
        if up:
            last_y = y + assigned_length
        else:
            last_y = y - assigned_length
        last_y = max( min( abs(y), vert_pic_size ), 0)
        assigned_length = abs(y - last_y)

        # Draw the line
        # over then up/down
        if right:
            print "over", res
            #draw(res,0)
        else:
            print "over", -res
            #draw(-res,0)
        if up:
            cur_y += assigned_length
            #draw(0,assigned_length)
            print "up", assigned_length
        else:
            cur_y -= assigned_length
            #draw(0,-assigned_length)
            print "down", -assigned_length
        right = not right
        
        # Condition for top or bottom of the board
        if last_y >= top_y or last_y <= start_y:
            print "changing direction"
            cur_x += HORIZONTAL_SPACE * res
            if right:
                print "right"
                #draw( HORIZONTAL_SPACE * res, 0 )
            else:
                print "left"
                #draw( (HORIZONTAL_SPACE-1) * res, 0 )
            up = not up

    print "ok, all done"
        
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
    time.sleep( 1.2 * dist/SPEED)
    

if __name__ == '__main__':
    main()
