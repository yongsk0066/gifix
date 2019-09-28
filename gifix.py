from PIL import Image
import numpy as np
import cv2
import math
import binascii
from textwrap import wrap


# img = Image.open("giphy.gif")

img = open("giphy.gif", 'r')

with open("giphy.gif", 'rb+') as f:
    string = f.read(6)
    print(string)
    p = binascii.b2a_hex(string)
    q = str(int(p))
    print(wrap(q,2))
