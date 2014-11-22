#!/usr/bin/env python

from PIL import Image
import numpy as np

size = 50,50
img = Image.open('testimg.png').convert('L')
img.thumbnail(size, Image.ANTIALIAS)


x_size, y_size = img.size

for x in range(x_size):
    print ''
    for y in range(y_size):
        print img.getpixel((x,y)),
