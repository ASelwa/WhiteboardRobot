#!/usr/bin/env python 

# Whiteboard CNC robot
# Winter 2014
# Badass residents of 83 D'Arcy 

import sys
import serial
import time

PORT = 9600

# Connect to arduino
device = "/dev/ttyAMC1"

def main():   
    global cur_x, cur_y, ser

    # Starting location
    cur_x = int(sys.argv[1])
    cur_y = -1*int(sys.argv[2])

    # Connect to arduino
    device = "/dev/ttyAMC1"
    try:
        ser = serial.Serial(device, PORT)
    except serial.SerialException:
        ser = serial.Serial('/dev/ttyACM0', PORT)
        time.sleep(2)
    finally:
        print 'Connected'

    while(1):
        try:
            points = raw_input('Enter points, separated by a space: ')
            points = points.split(' ')
            x = int(points[0])
            y = int(points[1])
        except ValueError:
            print 'Try again'
            continue
        draw(x,y)

def draw(x,y):
    global cur_x, cur_y, ser
    print x, y
    # The A is to verify that a real signal has been sent
    ser.write(str(int(cur_x))+','+str(int(cur_x+x))+','+
              str(int(cur_y))+','+str(int(cur_y+y))+'\n')
    # Update coordinates
    cur_x, cur_y = cur_x + x, cur_y + y
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
