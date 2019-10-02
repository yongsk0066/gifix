import binascii
from textwrap import wrap
import os

# img = Image.open("giphy.gif")
# img = open("giphy.gif", 'r')


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
# print(wrap(q[1600:1616], 2))
# print(wrap(q[1616:1680], 2))
# print(type(bin(int('0xFF', 16))))
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
    GCT = wrap(q[26:26 + header_dict['GCT_size'] * 2], 6)
    header_dict['GCT'] = GCT
    return header_dict


print(header_info(q))
