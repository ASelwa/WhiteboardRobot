#!/usr/bin/env python 

# Whiteboard CNC robot
# Winter 2014
# Badass residents of 83 D'Arcy 

import sys
import serial
import time
import subprocess
import math

SPEED = 25 # mm/s
PORT = 9600
SPACE = 2
LEFT_EDGE = 100
RIGHT_EDGE = 1800
TOP_EDGE = 100
BOTTOM_EDGE = 1000

# Connect to arduino
device = "/dev/ttyACM0"
device2 = "/dev/ttyAMC1"

def main():   
    global cur_x, cur_y, scale, ser

    # Starting location
    cur_x = int(sys.argv[1])
    cur_y = -1*int(sys.argv[2])
    scale = int(sys.argv[3])

    # Connect to arduino
    try:
        ser = serial.Serial(device, PORT)
        print device
    except serial.SerialException:
        ser = serial.Serial(device2, PORT)
        print device2
        time.sleep(1)
    finally:
        print 'Connected'

    time.sleep(1)
    draw(20,0)

def draw(x,y):
    global cur_x, cur_y, ser
    print x, y,
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
    time.sleep(dist/SPEED)
    

if __name__ == '__main__':
    main()
