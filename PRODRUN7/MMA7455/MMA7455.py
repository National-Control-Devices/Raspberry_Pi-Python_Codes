import smbus
import math
import time
bus =smbus.SMBus(1)
 

def writeAccl(register,value):
        bus.write_byte_data(0x1D , register, value)
        return -1

def readAcclx():
        Accl_l = bus.read_byte_data(0x1D,0x00)
        Accl_h = bus.read_byte_data(0x1D,0x01)
	Accl_total = (Accl_l | Accl_h <<8)
	return Accl_total  if Accl_total < 512 else Accl_total - 1024


def readAccly():
        Accl_l = bus.read_byte_data(0x1D,0x02)
        Accl_h = bus.read_byte_data(0x1D,0x03)
	Accl_total = (Accl_l | Accl_h <<8)
	return Accl_total  if Accl_total < 512 else Accl_total - 1024


def readAcclz():
        Accl_l = bus.read_byte_data(0x1D,0x04)
        Accl_h = bus.read_byte_data(0x1D,0x05)
	Accl_total = (Accl_l | Accl_h <<8)
	return Accl_total  if Accl_total < 512 else Accl_total - 1024


def accelDataTotal():
        atotal = (((readAcclx()**2)+(readAccly()**2)+(readAcclz()**2))**0.5)
        atotal = (atotal * 128)/ 10000
	return atotal


#initialise the Acclelerometer
writeAccl(0x16,0x01) 
writeAccl(0x06,0x00)

		
 
while True :
	#Read our Acclelerometer values
	Acclx = readAcclx()
	Accly = readAccly()
	Acclz = readAcclz()		
	print Acclx
	print Accly
	print Acclz
	
	
	##Convert Acclelerometer values to degrees
	AcclXangle =  (math.atan2(Accly,Acclz)+3.14)*57.3
	AcclYangle =  (math.atan2(Acclz,Acclx)+3.14)*57.3

	#If IMU is up the correct way, use these lines
        AcclXangle -= 180.0
	if AcclYangle > 90:
	        AcclYangle -= 270.0
	else:
		AcclYangle += 90.0


	print "AcclX Anglen : " ,AcclXangle
	print "AcclY Angle  : " ,AcclYangle
	print "Atotal       : " ,accelDataTotal(),"g" 
	print "****************************"
	time.sleep(0.5)
	
