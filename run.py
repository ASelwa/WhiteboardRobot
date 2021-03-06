#!/usr/bin/env python 

# Whiteboard CNC robot
# Winter 2014
# Badass residents of 83 D'Arcy 

import sys
import serial
import time
import gtk
import Queue

PORT = 9600

# Connect to arduino
device = "/dev/ttyAMC1"

def main():   
    global cur_x, cur_y, ser, scale, last_x, last_y, q, number
    last_x = 0
    last_y = 0
    
    # Starting location
    cur_x = int(sys.argv[1])
    cur_y = -1*int(sys.argv[2])
    scale = int(sys.argv[3])

    # Connect to arduino
    device = "/dev/ttyAMC0"
    try:
        ser = serial.Serial(device, PORT)
    except serial.SerialException:
        ser = serial.Serial('/dev/ttyACM0', PORT)
        time.sleep(2)
    finally:
        print 'Connected'

    number = 0
    
    win = gtk.Window()
    box = gtk.EventBox()
    area = gtk.DrawingArea()
    
    box.connect('button-press-event', onclick)
    box.connect('motion-notify-event', onclick)

    box.add(area)
    win.add(box)
    win.show_all()
    win.connect('destroy', lambda *x: gtk.main_quit() )

    gtk.main()

def onclick(box, event):
    global last_x, last_y, q, number
    delta_x = -scale*(last_x - event.x)
    delta_y = scale*(last_y - event.y)
    number += 1
    if (abs(delta_x) > 50) or (abs(delta_y) > 50):
        last_x = event.x
        last_y = event.y
        return
    else:
        if number%15 == 0:
            last_x = event.x
            last_y = event.y
            draw(delta_x, delta_y)

def draw(x,y):
    global cur_x, cur_y, ser, scale
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
