import binascii
from textwrap import wrap
import os
import json

# img = Image.open("giphy.gif")
# img = open("giphy.gif", 'r')

with open('test.txt', 'rb+') as f:
    length1 = os.path.getsize('test.lzw')

    # read file with size of length
    stringq = f.read(length1)

    # convert binary to hex
    pq = binascii.b2a_hex(stringq)
    # print(pq)

'''
Convert 2 bytes of hex data To U16
With little-endian Byte Order
'''


# input two bytes of hex data
# '74 01'
def h2h_int(hex_byte):
    # wrap by 2 digit
    # ['74', '01']
    hd = wrap(hex_byte, 2)

    # bind two byte of binary data with little-endian
    # 00000001 ( 0x01 ) + 01110100 ( 0x74 )
    whole_bin = '0b' + h2b_bin(hd[1]) + h2b_bin(hd[0])

    # convert to oct and return
    # '0b0000000101110100'
    return int(whole_bin, 2)


'''
One Byte of Hex Data To Full Binary(string)
'''


# input byte data(string)
# '74'
def h2b_bin(hex):
    # convert hex to oct and convert to binary(string)
    # remove '0b' from binary data
    # '1110100'
    bin_data = bin(int(hex, 16))[2:]

    # make bin_data into 8bits data
    # output looks like '01110100'
    if len(bin_data) != 8:
        return ('0' * (8 - len(bin_data)) + bin_data)
    else:
        return bin_data


# print(os.path.getsize("giphy.gif"))

'''
main operator
'''
file = "giphy.gif"
# open file and read as binary
with open(file, 'rb+') as f:
    # get size of file
    length = os.path.getsize(file)

    # read file with size of length
    string = f.read(length)

    # convert binary to hex
    p = binascii.b2a_hex(string)

    # refine data
    q = str(p)[2:-1]
    # qs = wrap(q, 2)
    # print(qs)


####################################################
# TEST PRINT
####################################################
#
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
#
####################################################

# header_info as dict
def header_info(q):
    header_dict = {}

    # gif type 'GIF87a' or 'GIF89a'
    header_dict['type'] = ''.join([chr(int('0x' + x, 16)) for x in wrap(q[0:12], 2)])

    # width and height
    header_dict['width'] = h2h_int(q[12:16])
    header_dict['height'] = h2h_int(q[16:20])

    # flags and other infos
    flag_info = h2b_bin(q[20:22])
    # Global Color Table flag
    header_dict['GCT_flag'] = flag_info[0]
    # Bit per Pixel
    header_dict['BpP'] = 2 ** int('0b' + flag_info[1:4], 2) + 1
    # Color Table Sort flag
    header_dict['CTS_flag'] = flag_info[4]
    # Global Color Table Size
    header_dict['GCT_size'] = 3 * 2 ** (int('0b' + flag_info[5:8], 2) + 1)
    # Background Color Index
    header_dict['BCI'] = q[22:24]
    # Pixel Aspect Ratio
    header_dict['PAR'] = q[24:26]

    # Global Color Table
    # 26 ~ size of Global Color Table
    GCT = wrap(q[26:26 + header_dict['GCT_size'] * 2], 6)
    header_dict['GCT'] = GCT

    header_dict['last_digit'] = 26 + header_dict['GCT_size'] * 2
    return header_dict


h_d = header_info(q)
l_d = h_d['last_digit']


# print(h_d['last_digit'])
# print(wrap(q[h_d['last_digit']:1568], 2))
# print(wrap(q[1568:1590], 2))
# print(''.join([chr(int('0x' + x, 16)) for x in wrap(q[1568:1590], 2)]))
# print(q[1590:1592])
# print(q[1592:1594])
# print(q[1594:1598])
# print(q[1598:1600])


def application_extension(q, d):
    dt = {}
    dt['Introducer'] = 21
    dt['Label'] = 'ff'
    dt['Block_size_f'] = 11
    dt['App_data'] = ''.join([chr(int('0x' + x, 16)) for x in wrap(q[6:6 + dt['Block_size_f'] * 2], 2)])
    dt['Block_size_s'] = 3
    dt['Extension_type'] = int('0x' + q[30:32], 16)
    dt['Repeat_count'] = h2h_int(q[32:36])
    dt['Terminator'] = q[36:38]
    dt['last_digit'] = d + 38

    return dt


def graphic_control_extension(q, d):
    dt = {}
    dt['Introducer'] = 21
    dt['Label'] = 'f9'
    dt['Block_size'] = 4
    dt['Bit_field'] = h2b_bin(q[6:8])
    dt['Delay_time'] = int('0x' + q[8:12], 16)
    dt['TCI'] = q[12:14]
    dt['Terminator'] = q[14:16]
    dt['last_digit'] = d + 16

    return dt


def image_block(q, d):
    dt = {}
    dt['Separator'] = '2c'
    dt['Left_position'] = h2h_int(q[2:6])
    dt['Right_position'] = h2h_int(q[6:10])
    dt['Width'] = h2h_int(q[10:14])
    dt['Height'] = h2h_int(q[14:18])
    dt['flag'] = q[18:24]
    a = 24 + 510
    dt['o1'] = q[a:a + 2]
    a += 512
    dt['o2'] = q[a:a + 2]
    a += 512
    dt['o3'] = q[a:a + 2]
    a += 512
    dt['o4'] = q[a:a + 2]
    # a += 512
    # dt['o5'] = q[a:a + 2]
    # a += 512
    # dt['o6'] = q[a:a + 2]
    # a += 512
    # dt['o7'] = q[a:a + 2]
    # a += 512
    # dt['o8'] = q[a:a + 2]
    # a += 512
    # dt['o9'] = q[a:a + 2]
    # a += 512
    # dt['o10'] = q[a:a + 2]
    # a += 512
    # dt['o11'] = q[a:a + 2]
    # a += 512
    # dt['o12'] = q[a:a + 2]
    # a += 512
    # dt['o13'] = q[a:a + 2]
    # a += 512
    # dt['o14'] = q[a:a + 2]
    # a += 512
    # dt['o15'] = q[a:a + 2]

    return dt


a_d = application_extension(q[l_d:l_d + 38], l_d)
print(json.dumps(h_d))
print(json.dumps(a_d))
l_d = a_d['last_digit']
g_d = graphic_control_extension(q[l_d:l_d + 16], l_d)
print(json.dumps(g_d))
l_d = g_d['last_digit']
# print(l_d + 534)
i_d = image_block(q[1616:700000], l_d)
print(type(json.dumps(i_d)))
# b = wrap(q[1638:200256],2)
# print(" ".join(wrap(q[2150:2662], 2)))

# i = 0
# c = 0
# while True:
#     j = int('0x'+b[i],16) + 1
#     i += j
#     c += 1
#     print(c, i,b[i])

# print(wrap(q[109070 -100:109070 + 10],2))
