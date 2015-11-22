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
	
	bus.write_byte(0x40,0xE0)
	time.sleep(0.5)

	reading_msb	=bus.read_byte(0x40)
	reading_lsb	=bus.read_byte(0x40)
	temprature = (( reading_msb << 8  | reading_lsb)) * (175.72 /65536) - 46.85
	print 'Temprature : ' 
	print temprature
	
while True:

	getreading()
	
	
	







