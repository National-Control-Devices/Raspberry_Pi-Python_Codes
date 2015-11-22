import time
import smbus
bus = smbus.SMBus(1)

def getreading(): 
	
	bus.write_byte(0x49,0x00)
	time.sleep(0.5)
	reading	= bus.read_i2c_block_data(0x49,0x00,2)
	temprature = (( reading[0] * 256) + (reading[1])) / 256.0
	print "Temprature :", temprature
	
while True:

	getreading()
	
	
	







