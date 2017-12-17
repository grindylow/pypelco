# Example program to control a PELCO-D-type camera mount, 
# specificall this seems to work well with a 
#   https://www.aliexpress.com/item/Pan-Tilt-motorized-rotation-bracket-stand-holder-PELCO-D-control-for-CCTV-IP-camera-module-RS232/32827664380.html

import serial
import codecs
import time
from pelco_mount import *
    
PORT = 'com4'
s = serial.Serial(PORT,timeout=.1,baudrate=2400)
print(s)
m = pelco_mount(PORT)



#s.write(m.msg_pan_right())

#s.write(m.msg_go_pre(18))
#s.write(m.msg_go_home())

s.write(m.msg_test_init())

# for speed in (SPEED_SLOW,SPEED_MEDIUM,SPEED_HIGH):
    # s.write(m.msg_set_speed(speed))
    # s.write(m.msg_pan_left())
    # time.sleep(1)
    # s.write(m.msg_pan_right())
    # time.sleep(1)
    
a = s.read(100)
print(a)

s.close()
