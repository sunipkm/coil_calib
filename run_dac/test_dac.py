#!/usr/bin/env python3

import serial
import numpy as np
#import matplotlib.pyplot as plt
import sys
import time

if len(sys.argv) < 2:
    print("Usage: ./test_dac.py <Serial Device File/COM Port>\n\n")
    sys.exit(0)

s = serial.Serial(sys.argv[1], 115200)

# print("# Opened serial port")

time.sleep(2)

count = 0
chn = 0

ofile = open("coil_data.csv", 'w')

for chn in range(3):
    # First ensure that all channels are off
    for x in range(3):
        val = x & 0x0003
        val <<= 12
        val &= 0xf000
        val |= 2048
        val &= 0xffff
        s.write(str(val).encode('utf-8'))
        s.flush()
        for i in range(10):
            s.readline()
    for count in range(0,4096,50):
        chn = chn & 0x0003  # 2 bit only!
        val = count & 0x0fff  # 12 bit only!
        val |= chn << 12  # shift chn by 12 bits
        val &= 0xffff  # make sure it is 16 bits
        s.write(str(val).encode('utf-8'))
        s.flush()
        x = 0.0
        y = 0.0
        z = 0.0
        vx = 0.0
        vy = 0.0
        vz = 0.0
        for i in range(10):
            #expected to read 10 times
            vals = (s.readline()).decode('utf-8')
            # x_ = int.from_bytes(vals[0:2], byteorder='little', signed = True)
            # y_ = int.from_bytes(vals[2:4], byteorder='little', signed = True)
            # z_ = int.from_bytes(vals[4:6], byteorder='little', signed = True)
            words = vals.rstrip("\n").split()
            x_ = float(words[0])
            y_ = float(words[1])
            z_ = float(words[2])
            print(chn, count, x_, y_, z_, sep=',')
            x += x_
            vx += x_*x_
            y += y_
            vy += y_*y_
            z += z_
            vz += z_*z_
        ofile.write('%d,%d,%f,%f,%f,%f,%f,%f\n'%(chn,count,x/10,y/10,z/10,vx/10,vy/10,vz/10))
        # First ensure that all channels are off
    for x in range(3):
        val = x & 0x0003
        val <<= 12
        val &= 0xf000
        val |= 2048
        val &= 0xffff
        s.write(str(val).encode('utf-8'))
        s.flush()
        for i in range(10):
            s.readline()

s.close()
ofile.close()