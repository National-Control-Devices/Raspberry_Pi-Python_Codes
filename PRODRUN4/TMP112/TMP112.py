import time
import smbus
bus = smbus.SMBus(1)

def setup():

	bus.write_byte_data(0x48,0x01,0x00)

def reading():

       result = bus.read_i2c_block_data(0x48,0x00,2)
       temp = (result[0] << 8) + result[1]
       temp = (temp >> 4) & 0xfff0
       temp = temp * 0.0625
       time.sleep(.5)
       print temp
       

while True:

	setup()
	reading()