import time
import smbus
bus = smbus.SMBus(1)
address = 0x28

def getreading(): 
	command = [0xB0,0x00,0x00]
	bus.write_i2c_block_data(0x28,3, command)
	time.sleep(0.5)
	reading	=bus.read_i2c_block_data(0x28,0x00,4)
	humidity = ((reading[0] & 0x3F) * 256 + reading[1]) * (100.0/ 16383.0)
        print humidity	
	temprature = (( reading[2] * 256 + (reading[3] & 0xFC)) / 4 ) * (165.0 / 16383) - 40
	print temprature
	
while True:

	getreading()
	
	
	







