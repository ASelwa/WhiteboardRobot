#!/usr/bin/env python 

#
# Whiteboard CNC robot
# Winter 2014
# Badass residents of 83 D'Arcy 
#
# Communicates with Arduino over serial port to print.
#

import sys
import serial
import time
# https://pypi.python.org/pypi/dxfgrabber
import dxfgrabber # for reading in dxf files

# serial port for arduino: check this in 
# Tools->Serial Port in your arduino sketch
# SET THESE!
PORT = 9600

# Longest length in the drawing
MAXDIM = 300

# Starting location
# TODO pass these numbers 
xStart = int(sys.argv[1])
yStart = -1*int(sys.argv[2])

def main():
    # Connect to arduino
    device = "/dev/ttyAMC1"
    try:
        ser = serial.Serial(device, PORT)
    except serial.SerialException:
        ser = serial.Serial('/dev/ttyACM0', PORT)
        #print 'Oops, couldn\'t connect to the Arduino'
        #print 'is it plugged in?'
        #print 'did you set the right DEVICE and PORT in this file?'
        #exit()
        # Wait for arduino to connect
        time.sleep(2)
        print 'Connected'

    # Open dxf file
    filename = 'line.dxf'
    dxf = dxfgrabber.readfile(filename)
    lines = [ [],[],[],[] ]
    print 'x1 x2 y1 y2'
    # Get lines
    for entity in dxf.entities:
        x1,y1 = entity.start
        x2,y2 = entity.end
        print x1,x2,y1,y2
        lines[0].append(x1)
        lines[1].append(x2)
        lines[2].append(y1)
        lines[3].append(y2)
        
    # shift drawing so that origin is at 0,0
    x1Min = min(lines[0])
    x2Min = min(lines[1])
    y1Min = min(lines[2])
    y2Min = min(lines[3])
    xMin = min([x1Min, x2Min])
    yMin = min([y1Min, y2Min])
    lines[0] = [el - xMin for el in lines[0]]
    lines[1] = [el - xMin for el in lines[1]]
    lines[2] = [el - yMin for el in lines[2]]
    lines[3] = [el - yMin for el in lines[3]]

    # Scale drawing so that maximum dimension is MAXDIM
    x1Max = max(lines[0])
    x2Max = max(lines[1])
    y1Max = max(lines[2])
    y2Max = max(lines[3])
    Max = max([x1Max, x2Max, y1Max, y2Max])
    lines[0] = [ (el)*(MAXDIM/Max)+xStart for el in lines[0] ]
    lines[1] = [ (el)*(MAXDIM/Max)+xStart for el in lines[1] ]
    lines[2] = [ (el)*(MAXDIM/Max)+yStart for el in lines[2] ]
    lines[3] = [ (el)*(MAXDIM/Max)+yStart for el in lines[3] ]

    # Invert y coordinate because 'y' is backwards on board
    lines[2] = [ e *(-1) for e in lines[2] ]
    lines[3] = [ e *(-1) for e in lines[3] ]

    print 'after'
    # Draw lines
    for x1,x2,y1,y2 in zip(lines[0],lines[1],lines[2],lines[3]):
        print x1,x2,y1,y2
        # The A is to verify that a real signal has been sent
        ser.write(str(int(x1))+','+str(int(x2))+','+str(int(y1))+','+str(int(y2))+'\n')
        # Wait for the arduino to finish the line or break after a while
        millis = int(round(time.time() * 1000))
        print millis
        while(1):
            try:
                # TODO: wrap this call in something that will kill it if it's
                # not done in a few milliseconds
                waitline = ser.read()
            except: # serial.SerialException:
                print "Something wrong with serial connection?"
                break
            finally:
                break
            if waitline == "a":
                break
            current_millis = int(round(time.time() * 1000))
            # Timeout condition
            print current_millis
            if current_millis > millis + 2000:
                print "Timeout"
                break

    # To draw line:
    # ser.write('x1,x2,y1,y2\n')

if __name__ == "__main__":
    main()
