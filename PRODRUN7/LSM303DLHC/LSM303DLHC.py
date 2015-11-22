import smbus
import time
import math
bus = smbus.SMBus(1)



def Write_Accl(register,value):
        bus.write_byte_data(0X19 , register, value)
        return -1

def Write_Mag(register,value):
        bus.write_byte_data(0x1E, register, value)
        return -1



def readAcclx():
        Accl_l = bus.read_byte_data(0X19,0x28)
        Accl_h = bus.read_byte_data(0X19,0x29)
	Accl_total = (Accl_l | Accl_h <<8)
	return Accl_total>>4  if Accl_total < 32768 else Accl_total - 65536


def readAccly():
        Accl_l = bus.read_byte_data(0X19,0x2A)
        Accl_h = bus.read_byte_data(0X19,0x2B)
	Accl_total = (Accl_l | Accl_h <<8) 
	return Accl_total>>4  if Accl_total < 32768 else Accl_total - 65536


def readAcclz():
        Accl_l = bus.read_byte_data(0X19,0x2C)
        Accl_h = bus.read_byte_data(0X19,0x2D)
	Accl_total = (Accl_l | Accl_h <<8) 
	return Accl_total>>4  if Accl_total < 32768 else Accl_total - 65536

def accelDataTotal():
        atotal = (((readAcclx()**2)+(readAccly()**2)+(readAcclz()**2))**0.5)
        atotal = atotal / 1000
	return atotal


def readMagx():
        Mag_l = bus.read_byte_data(0x1E,0x03)
        Mag_h = bus.read_byte_data(0x1E,0x04)
        Mag_total = (Mag_l | Mag_h <<8)
        return Mag_total  if Mag_total < 32768 else Mag_total - 65536


def readMagy():
        Mag_l = bus.read_byte_data(0x1E,0x07)
        Mag_h = bus.read_byte_data(0x1E,0x08)
        Mag_total = (Mag_l | Mag_h <<8)
        return Mag_total  if Mag_total < 32768 else Mag_total - 65536


def readMagz():
        Mag_l = bus.read_byte_data(0x1E,0x05)
        Mag_h = bus.read_byte_data(0x1E,0x06)
        Mag_total = (Mag_l | Mag_h <<8)
        return Mag_total  if Mag_total < 32768 else Mag_total - 65536


def MagDataTotal():
        mtotal = (((readMagx()**2)+(readMagy()**2)+(readMagz()**2))**0.5)
        mtotal = (mtotal)/84000
	return mtotal


#initialise the Acclelerometer
Write_Accl(0X20, 0x27) 
Write_Accl(0X23, 0x00)
#initialise the Magnetometer
Write_Mag(0X02, 0x00)
Write_Mag(0X01, 0x20)
Write_Mag(0x00,0x80)

while True:
	
	#Read our Acclelerometer,gyroscope and Magnetometer  values
	Acclx = readAcclx()
	Accly = readAccly()
	Acclz = readAcclz()
	Magx = readMagx()
	Magy = readMagy()
	Magz = readMagz()

	#Calculate heading
	heading = 180 * math.atan2(Magy,Magx)/3.14

	if heading < 0:
	 	heading += 360


	print "Atotal       : " ,accelDataTotal(),"g" 
	print "Mtotal       : " ,MagDataTotal(),"Guass"
 	print "HEADING      : " ,heading
	print "****************************"
        time.sleep(0.5)
	
