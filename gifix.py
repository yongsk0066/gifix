from PIL import Image
import numpy as np
import cv2
import math
import binascii
from textwrap import wrap
import os.path

# img = Image.open("giphy.gif")
# img = open("giphy.gif", 'r')
type_end = 6
width_start = 6
height_start = 8

'''
Convert 2 bytes of hex data To U16
With little-endian Byte Order
'''


def h2h_int(hd):
    wholeBin = '0b' + h2b_bin(hd[1]) + h2b_bin(hd[0])
    return int(wholeBin, 2)


'''
One Byte of Hex Data To Full Binary(string)
'''


def h2b_bin(hex):
    binData = bin(int(hex, 16))[2:]
    if len(binData) != 8:
        return ('0' * (8 - len(binData)) + binData)
    else:
        return binData


'''
main operator
'''
with open("giphy.gif", 'rb+') as f:
    string = f.read(20)
    # print(string)
    p = binascii.b2a_hex(string)
    # print(p)
    q = str(p)[2:].replace("'", '')
    qs = wrap(q, 2)
    # print(qs[:6])
'''
file type
'''
print(str(string[:type_end]).replace("'", '')[1:])
print(h2h_int(qs[width_start:width_start + 2]))
print(h2h_int(qs[height_start:height_start + 2]))
