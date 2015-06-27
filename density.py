#!/usr/bin/env python

# Whiteboard CNC robot
# Winter 2014
# Badass residents of 83 D'Arcy

import sys
import serial
import time
import subprocess
import math
from PIL import Image, ImageDraw

SPEED = 30 # mm/s
PORT = 9600
MAX_PIC_SIZE = 1600, 1600
THRESH = 0.1
HOR_RES = 5

device = "/dev/ttyACM1"
device2 = "/dev/ttyACM0"

def main():
    global cur_x, cur_y, ser

    # Connect to arduino
    try:
#        ser = serial.Serial(device, PORT)
        print 'Connected to ', device
    except OSError:
        ser = serial.Serial(device2, PORT)
        print 'Connected to ', device2
        time.sleep(1)

    # Get the pic
    imagename = 'roy.jpg'
    img = Image.open(imagename).convert('L') # greyscale

    # Keep a high res version for annotating lines on top of
    #img_high_res = Image.open(imagename)
    img_high_res = Image.new("RGB",img.size,'white')
    annotation = ImageDraw.Draw(img_high_res)

    print 'IMAGE SIZE hor_pic_size: ', img.size[0], 'vert_pic_size: ', img.size[1]
    img.thumbnail(MAX_PIC_SIZE, Image.ANTIALIAS)
    hor_pics, vert_pics = img.size
    print 'AFTER SCALING hor_pics: ', hor_pics, 'vert_pics: ', vert_pics

    # Full size picture to thumbnail conversion
    image_scale = img_high_res.size[0] / float(hor_pics)

    # User inputs, remember that y is -'ve in my coor system but +'ve in pixel space
    start_x = input('current x position in mm: ')
    start_y = input('current y position in mm: ')
    end_x = input('end x position in mm: ')
    end_y = input('end y position in mm: ')

    # For a completely white pixel, what is the distance in pixels?
    max_distance_pixels = vert_pics * 1

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

    # Delta distance in mm
    del_x = abs(done_x - start_x)
    del_y = abs(done_y - start_y)

    # Conversion factor between pixels and mm
    scale = del_x / float(hor_pics)

    # Starting Conditions
    cur_x = start_x
    cur_y = start_y
    x = 0
    y = 0
    right = True
    up = False

    # Draw the picture
    while x < hor_pics:
        print "~~~~~"
        # get the x, y location in pixel space
        #x = int( ( (cur_x - start_x) / float(del_x) ) * hor_pics )
        print "x: ", x
        #y = abs(int( ( (cur_y - start_y) / float(del_y) ) * hor_pics ))
        print "y: ", y

        # Lookup Density Value, black gets mapped to 0 by getpixel()
        density = 1 - (img.getpixel((x,y)) / float(255))
        print "pixel density: ", density

        # Calculate line length
        distance = int( max_distance_pixels * (1 - density) )
        #distance = vert_pics
        print "calculated distance", distance

        # We have to go forward at minimum one pixel
        distance = max(1, distance)

        # Edge case for the edge of the picture
        if up:
            distance = min(distance, y)
        else:
            distance = min(distance, vert_pics - 1 - y)
        print "distance: ", distance

        if up:
            distance *= -1

        # Cut the distance short if there is an abrupt change in darkness
        for i in range(abs(distance)):
            if up: i *= -1
            new_density = (1 - img.getpixel((x,y+i))/float(255))
            if abs(new_density - density) > THRESH:
                distance = i
                break

        if up: color = 'blue'
        else: color = 'red'
        # Move the marker
        draw(0, scale*distance)
        annotation.line( (int(x*image_scale),
                          int(y*image_scale),
                          int(x*image_scale),
                          int((y+distance)*image_scale)), fill=color)

        # update coordinates
        y += distance

        # if we're at the top, then move over
        if y == 0 or y == vert_pics - 1:
            if right:
                pass
                draw(scale * (1 + HOR_RES), 0)
                annotation.line( (int(x*image_scale),
                                  int(y*image_scale),
                                  int((x+HOR_RES+1)*image_scale),
                                  int((y)*image_scale)), fill=color)
                x += HOR_RES + 1
            else:
                draw(scale * 1, 0)
                annotation.line( (int(x*image_scale),
                                  int(y*image_scale),
                                  int((x+1)*image_scale),
                                  int((y)*image_scale)), fill=color)
                x += 1
                right = True
            up = not up
            continue

        # move sideways
        if right:
            pass
            draw(scale * HOR_RES, 0)
            annotation.line( (int(x*image_scale),
                              int(y*image_scale),
                              int((x+HOR_RES)*image_scale),
                              int(y*image_scale)), fill=color)
            x += HOR_RES
        else:
            pass
            draw(-scale * HOR_RES, 0)
            annotation.line( (int(x*image_scale),
                              int(y*image_scale),
                              int((x-HOR_RES)*image_scale),
                              int(y*image_scale)), fill=color)
            x -= HOR_RES
        right = not right

    print "ok, all done"
    img_high_res.show()

def draw(x,y):
    return
    global cur_x, cur_y, ser
    ser.write(str(int(cur_x))+','+str(int(cur_x+x))+','+
              str(int(cur_y))+','+str(int(cur_y+y))+'\n')
    print str(int(cur_x))+','+str(int(cur_x+x))+','+ str(int(cur_y))+','+str(int(cur_y+y))
    # Update coordinates
    cur_x, cur_y = cur_x + x, cur_y + y
    dist = math.sqrt( x**2 + y**2 )
    time.sleep( 1.3 * dist/SPEED)

if __name__ == '__main__':
    main()
