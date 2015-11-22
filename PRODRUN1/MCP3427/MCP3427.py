# Read MCP3427 12-Bit, Multi-Channel Analog-to-Digital Converter with I2C Interface and On-Board Reference using Raspberry Pi


import smbus
import time
bus = smbus.SMBus(1)


def getadcreading() :
	data = bus.read_i2c_block_data(0x68,0x00,2)
	t = ((data[0] << 8) | data[1])
	if (t >= 32768):
		t = 65536 -t
	v = t * 2.048/2048	
	print "Voltage of the Source is : ", v,"volts"
		
	time.sleep(1)

# Default :Channel 1,Sample Rate 240SPS(12- bit),Gain x1 Selected
bus.write_byte(0x68,0x90)

while True:

	getadcreading()