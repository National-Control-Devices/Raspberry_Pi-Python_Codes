import time
import math
import smbus
bus = smbus.SMBus(1)

def fetchData():

	LSB = bus.read_byte(0x0e)
        MSB = bus.read_byte(0x0e)
        time.sleep(0.5)
      	#MSB = data[0]  
     	#LSB = data[1] 
	print MSB
	print LSB
	raw_angle = MSB  << 8 | LSB 
	raw_angle =  raw_angle >> 4
	angle = (360 * raw_angle) / 4096.0     
    	print angle
	return angle


while True : 

        fetchData()
       

   

 


