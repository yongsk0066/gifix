from PIL import Image
import numpy as np
import cv2
import math
import binascii
from textwrap import wrap
import os.path
import os

# img = Image.open("giphy.gif")
# img = open("giphy.gif", 'r')

type_end = 6
width_start = 6 * 2
height_start = 8 * 2

'''
Convert 2 bytes of hex data To U16
With little-endian Byte Order
'''


# input two bytes of hex data
def h2h_int(hex_byte):
    # wrap by 2 digit
    hd = wrap(hex_byte, 2)

    # bind two byte of binary data with little-endian
    whole_bin = '0b' + h2b_bin(hd[1]) + h2b_bin(hd[0])

    # convert to oct and return
    return int(whole_bin, 2)


'''
One Byte of Hex Data To Full Binary(string)
'''


# input byte data(string)
def h2b_bin(hex):
    # convert hex to oct and convert to binary(string)
    # remove '0b' from binary data
    bin_data = bin(int(hex, 16))[2:]

    # make bin_data into 8bits data
    # output looks like '00100111'
    if len(bin_data) != 8:
        return ('0' * (8 - len(bin_data)) + bin_data)
    else:
        return bin_data


# print(os.path.getsize("giphy.gif"))

'''
main operator
'''
file = "giphy.gif"

with open(file, 'rb+') as f:
    length = os.path.getsize(file)
    # print(length)
    string = f.read(length)
    # print(type(string))
    p = binascii.b2a_hex(string)
    q = str(p)[2:-1]
    # qs = wrap(q, 2)
    # print(qs)
'''
file type
'''
# print(str(string[:type_end]).replace("'", '')[1:])
# print(''.join([chr(int('0x' + x, 16)) for x in wrap(q[0:12], 2)]))
# print(h2h_int(q[width_start:width_start + 4]))
# print(h2h_int(q[height_start:height_start + 4]))
# print(h2b_bin(q[20:22]))
# print(q[22:24])
# print(q[24:26])
# print(wrap(q[26:1562], 6))
# print(256* 3 * 2 + 26)
# print(wrap(q[1562:1600], 2))
# print(wrap(q[1600:1616], 2))
# print(wrap(q[1616:1680], 2))
#
# print(type(bin(int('0xFF', 16))))

def header_info(q):
    header_dict = {}
    header_dict['type'] = ''.join([chr(int('0x' + x, 16)) for x in wrap(q[0:12], 2)])
    header_dict['width'] = h2h_int(q[12:16])
    header_dict['height'] = h2h_int(q[16:20])

    flag_info = h2b_bin(q[20:22])
    header_dict['GCT_flag'] = flag_info[0]
    header_dict['BpP'] = 2 ** int('0b' + flag_info[1:4], 2) + 1
    header_dict['CTS_flag'] = flag_info[4]
    header_dict['GCT_size'] = 3 * 2 ** (int('0b' + flag_info[5:8], 2) + 1)
    header_dict['BCI'] = q[22:24]
    header_dict['PAR'] = q[24:26]

    GCT = wrap(q[26:26 + header_dict['GCT_size'] * 2], 6)
    header_dict['GCT'] = GCT
    return header_dict


print(header_info(q))
