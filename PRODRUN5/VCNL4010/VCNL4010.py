#!/usr/bin/python

import time
import math
import smbus
bus= smbus.SMBus(1)

# Read data from proximity sensor
def read_proximity():
	bus.write_byte_data(0x13,0x80, 0x08)
    	while True:
      		result = bus.read_byte_data(0x13,0x80)
      		if (result & 0x20):
        		return bus.read_word_data(0x13,0x87)
      	time.sleep(0.5)
	
# Read data from ambient sensor  
def read_ambient():
	bus.write_byte_data(0x13,0x80, 0x10)
    	while True:
      		result = bus.read_byte_data(0x13,0x80)
      		if (result & 0x40):
        		return bus.read_word_data(0x13,0x85)
      	times.leep(0.5)
	



#Write proximity adjustement register
bus.write_byte_data(0x13,0x8A, 0x81)


while True :
	time.sleep(0.5)
	proximity = read_proximity()
	ambient =read_ambient()
	print "Proximity :",proximity
	print "Ambient :",ambient