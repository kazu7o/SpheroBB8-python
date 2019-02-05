#!/usr/bin/env python
from bluepy import btle
import BB8_simple
import readchar
import sys

bb8 = BB8_simple.BB8Controller()
while True:
    kb = readchar.readchar()
    #sys.stdout.write(kb)
    if kb == 'w':
        bb8.go_forward()
    if kb == 'a':
        bb8.go_left()
    if kb == 's':
        bb8.go_back()
    if kb == 'd':
        bb8.go_right()
    if kb == 'q':
        print("Stop...")
        sys.exit()
