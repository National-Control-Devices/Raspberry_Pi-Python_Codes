import smbus
import time
import math
bus = smbus.SMBus(1)



def writeAccl(register,value):
        bus.write_byte_data(0x18 , register, value)
        return -1


def readAcclx():
        Accl_l = bus.read_byte_data(0x18,0x28)
        Accl_h = bus.read_byte_data(0x18,0x29)
	Accl_total = (Accl_l | Accl_h <<8)
	return Accl_total  if Accl_total < 32768 else Accl_total - 65536


def readAccly():
        Accl_l = bus.read_byte_data(0x18,0x2A)
        Accl_h = bus.read_byte_data(0x18,0x2B)
	Accl_total = (Accl_l | Accl_h <<8)
	return Accl_total  if Accl_total < 32768 else Accl_total - 65536


def readAcclz():
        Accl_l = bus.read_byte_data(0x18,0x2C)
        Accl_h = bus.read_byte_data(0x18,0x2D)
	Accl_total = (Accl_l | Accl_h <<8)
	return Accl_total  if Accl_total < 32768 else Accl_total - 65536

def accelDataTotal():
        atotal = (((readAcclx()**2)+(readAccly()**2)+(readAcclz()**2))**0.5)
        atotal = (atotal / 32768) * 2
	return atotal

#initialise the Acclelerometer
writeAccl(0x20,0x27) 
writeAccl(0x23,0x00) 


while True:
	
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
        AcclXangle -= 180.0
	if AcclYangle > 90:
	        AcclYangle -= 270.0
	else:
		AcclYangle += 90.0

	#Normalize Acclelerometer raw values.
        AcclXnorm = Acclx/math.sqrt(Acclx * Acclx + Accly * Accly + Acclz * Acclz)
	AcclYnorm = Accly/math.sqrt(Acclx * Acclx + Accly * Accly + Acclz * Acclz)

	print "Atotal       : " ,accelDataTotal(),"g" 
 	print "AcclX Anglen : " ,AcclXangle
	print "AcclY Anglen : " ,AcclYangle
	print "****************************"
        time.sleep(0.5)
	
