#!/usr/bin/env python

# Whiteboard CNC robot
# Summer 2015
# Phil Lsaac

# Goes up and down squiggling back and forth at a constant horizontal distance

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
HOR_LINES = 40 # How far to go sideways
MIN_DIST = 5

# It switches back and forth between these so try both
device = "/dev/ttyACM1"
device2 = "/dev/ttyACM0"

def main():
    ###############################
    # SETUP
    ###############################

    global cur_x, cur_y, ser

    # Get arguments
    if len(sys.argv) < 5:
        print "Useage: [sudo] draw_jpg.py filename.jpg start_x end_x start_y end_y [horizontal_lines]"
        return
    imagename = sys.argv[1]
    start_x = int(sys.argv[2])
    end_x = int(sys.argv[3])
    start_y = int(sys.argv[4])
    end_y = int(sys.argv[5])
    if len(sys.argv) > 5:
        HOR_LINES = int(sys.argv[6])

    # Connect to arduino
    fake = raw_input('connect to arduino? [y/n]: ')
    if fake.lower() == 'y':
        fake = False
    else:
        fake = True

    if not fake:
        print 'connecting'
        try:
            try:
                ser = serial.Serial(device, PORT)
                print 'Connected to ', device
            except OSError:
                ser = serial.Serial(device2, PORT)
                print 'Connected to ', device2
                time.sleep(1)
            print 'connected to arduino'
        except OSError:
            print '[ERROR] Root permissions may be required to access USB port.'
            return

    else:
        print 'running simulation only'

    # Get the pic
    print 'getting image ', imagename
    img = Image.open(imagename).convert('L') # greyscale

    # Keep a high res version for annotating lines on top of
    #img_high_res = Image.open(imagename)
    img_high_res = Image.new("RGB",img.size,'white') # blank canvas
    annotation = ImageDraw.Draw(img_high_res)

    ''' WHY THE FUCK DID I DO THIS???
    print 'IMAGE SIZE hor_pic_size: ', img.size[0], 'vert_pic_size: ', img.size[1]
    img.thumbnail(MAX_PIC_SIZE, Image.ANTIALIAS)
    hor_pics, vert_pics = img.size
    print 'AFTER SCALING hor_pics: ', hor_pics, 'vert_pics: ', vert_pics
    '''
    print 'IMAGE SIZE hor_pic_size: ', img.size[0], 'vert_pic_size: ', img.size[1]
    hor_pics, vert_pics = img.size

    # Length of horizontal lines
    HOR_RES = int(hor_pics/HOR_LINES)

    # Full size picture to thumbnail conversion
    image_scale = img_high_res.size[0] / float(hor_pics)

    # For a completely white pixel, what is the distance in pixels?
    max_distance_pixels = int(vert_pics * 0.5)

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

    # Starting Conditions. Starts at top left which is 0,0 in the
    # coordinate system. Y is positive downwards
    cur_x = start_x
    cur_y = start_y
    x = 0
    y = 0
    right = True
    up = False

    lines = [] # Hold all the lines here and draw them later
    t = 0
    line_num = 0
    print 'running simulation'

    #############################
    # Simulate the picture GOGOGO
    #############################
    while x < hor_pics:
        # Lookup Density Value, black gets mapped to 0 by getpixel()
        density = 1 - (img.getpixel((x,y)) / float(255))

        # Calculate line length
        distance = int( max_distance_pixels * (1 - density) )

        # We have to go forward at minimum one pixel
        distance = max(MIN_DIST, distance)

        # Edge case for the edge of the picture
        if up:
            distance = min(distance, y)
        else:
            distance = min(distance, vert_pics - 1 - y)

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
        # add line
        lines.append((0, scale*distance))
        t = fakeDraw(0, scale*distance, t)
        annotation.line( (int(x*image_scale),
                          int(y*image_scale),
                          int(x*image_scale),
                          int((y+distance)*image_scale)), fill=color)

        # update coordinates
        y += distance

        # if we're at the top, then move over
        if y == 0 or y == vert_pics - 1:
            if right:
                # Print out % done
                print line_num*100/float(HOR_LINES), "%"
                line_num += 1

                lines.append((scale * (1 + HOR_RES), 0))
                t = fakeDraw((scale * (1 + HOR_RES)), 0, t)
                annotation.line( (int(x*image_scale),
                                  int(y*image_scale),
                                  int((x+HOR_RES+1)*image_scale),
                                  int((y)*image_scale)), fill=color)
                x += HOR_RES + 1
            else:
                # print out % done
                print line_num*100/float(HOR_LINES), "%"
                line_num += 1

                lines.append((scale * 1, 0))
                t = fakeDraw(scale*1, 0, t)
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
            lines.append((scale * HOR_RES, 0))
            t = fakeDraw( scale*HOR_RES, 0, t)
            annotation.line( (int(x*image_scale),
                              int(y*image_scale),
                              int((x+HOR_RES)*image_scale),
                              int(y*image_scale)), fill=color)
            x += HOR_RES
        else:
            lines.append((-scale * HOR_RES, 0))
            t = fakeDraw( -scale*HOR_RES, 0, t)
            annotation.line( (int(x*image_scale),
                              int(y*image_scale),
                              int((x-HOR_RES)*image_scale),
                              int(y*image_scale)), fill=color)
            x -= HOR_RES
        right = not right

    print 'done simulation'
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    img_high_res.show()

    # Now actually draw it
    cur_x = start_x
    cur_y = start_y

    print 'Time estimate: ', t/60, ' minutes'
    print 'Number of segments: ', len(lines)

    if fake:
        return

    else:
        proceed = raw_input('Draw outline? [y/n]: ')
        if proceed.lower() == 'y':
            print 'yeah!'
            # TODO SOMETHING HERE SEEMS FUNKS
            draw(del_x, 0)
            draw(0, del_y)
            draw(-del_x, 0)
            draw(0, -del_y)

        proceed = raw_input('go for it? [y/n]: ')
        if proceed.lower() == 'y':
            print 'going for it'
            for line in lines:
                draw(line[0], line[1])
        return

################################################################################

def fakeDraw(x,y,t):
    global cur_x, cur_y, ser
    # Update coordinates
    cur_x, cur_y = cur_x + x, cur_y + y
    dist = math.sqrt( x**2 + y**2 )
    t = t + 1.3 * dist/SPEED
    return t

def draw(x,y):
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
