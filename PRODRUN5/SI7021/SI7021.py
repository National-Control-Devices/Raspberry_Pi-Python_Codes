import time
import smbus
bus = smbus.SMBus(1)

def getreading(): 
	
	bus.write_byte(0x40,0xE5)
	time.sleep(0.5)
	reading_msb	=bus.read_byte(0x40)
	reading_lsb	=bus.read_byte(0x40)
		
	humidity = ((reading_msb << 8  | reading_lsb) * 125.0/ 65536.0)   - 6.0
        print 'Humidity :' 
	print humidity
	
	
while True:

	getreading()
	
	
	







