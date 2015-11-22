import time
import smbus
bus= smbus.SMBus(1)

def intiate():
	
		bus.write_byte_data(0x18,0x01,0x00)
		return 0

def readTempC():
 
	time.sleep(0.5)
	read=bus.read_i2c_block_data(0x18,0x05,2)
	read1 = (read[0] & 0x0F) << 4
	read2 = read1+ (read[1] >> 4)
	print read2
	return read2



while True:

	intiate()
	readTempC()

