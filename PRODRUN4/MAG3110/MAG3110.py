import smbus
import time
import math
bus = smbus.SMBus(1)



def writeMag(register,value):
        bus.write_byte_data(0x0E, register, value)
        return -1

def readMagx():
        Mag_l = bus.read_byte_data(0x0E,0x01)
        Mag_h = bus.read_byte_data(0x0E,0x02)
        Mag_total = (Mag_l | Mag_h <<8)
        return Mag_total  if Mag_total < 32768 else Mag_total - 65536


def readMagy():
        Mag_l = bus.read_byte_data(0x0E,0x03)
        Mag_h = bus.read_byte_data(0x0E,0x04)
        Mag_total = (Mag_l | Mag_h <<8)
        return Mag_total  if Mag_total < 32768 else Mag_total - 65536


def readMagz():
        Mag_l = bus.read_byte_data(0x0E,0x05)
        Mag_h = bus.read_byte_data(0x0E,0x06)
        Mag_total = (Mag_l | Mag_h <<8)
        return Mag_total  if Mag_total < 32768 else Mag_total - 65536


def MagDataTotal():
        mtotal = (((readMagx()**2)+(readMagy()**2)+(readMagz()**2))**0.5)
        mtotal = (mtotal* 0.1) / 10000
	return mtotal





while True:

	
	#initialise the Magnetometer
	writeMag(0X10, 0x81)
	writeMag(0X11, 0x80)	
	bus.read_byte_data(0x0E,0x08) 
	
	#Read our  Magnetometer  values
	Magx = readMagx()
	Magy = readMagy()
	Magz = readMagz()	
	print Magx
	print Magy
	print Magz
	
	

	#Calculate heading
	heading = 180 * math.atan2(Magy,Magx)/3.14

	if heading < 0:
	 	heading += 360

	print "Mtotal       : " ,MagDataTotal(),"Guass"
 	print "HEADING      : " ,heading
	print "****************************"
        time.sleep(0.5)
	
