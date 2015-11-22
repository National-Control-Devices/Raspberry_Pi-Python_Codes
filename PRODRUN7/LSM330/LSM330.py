import smbus
import time
import math

bus = smbus.SMBus(1)



def accelDatax():
        axhi = bus.read_byte_data(0x1E, 0X28)
        axlo = bus.read_byte_data(0x1E, 0X29)
        axtotal = ((axhi << 8) | axlo)
	if axtotal > 32768 :
		axtotal = axtotal - 65536 
	return axtotal

def accelDatay():
        ayhi = bus.read_byte_data(0x1E, 0X2A)
        aylo = bus.read_byte_data(0x1E, 0X2B)
        aytotal = ((ayhi << 8) | aylo)
	if aytotal > 32768 :
		aytotal = aytotal - 65536 
        return aytotal

def accelDataz():
        azhi = bus.read_byte_data(0x1E, 0X2C)
        azlo = bus.read_byte_data(0x1E, 0X2D)
        aztotal = ((azhi << 8) | azlo)
	if aztotal > 32768 :
		aztotal = aztotal - 65536 
        return aztotal


def accelDataTotal():
        atotal = (((accelDatax()**2)+(accelDatay()**2)+(accelDataz()**2))**0.5)
        atotal = (atotal / 32768)
	return atotal


def GyroDatax():
        hxhi = bus.read_byte_data(0x6A, 0X28)
        hxlo = bus.read_byte_data(0x6A, 0X29)
        hxtotal = ((hxhi << 8) | hxlo)
	if hxtotal > 32768 :
		hxtotal = hxtotal - 65536 
        return hxtotal

def GyroDatay():
        hyhi = bus.read_byte_data(0x6A, 0X2A)
        hylo = bus.read_byte_data(0x6A, 0X2B)
        hytotal = ((hyhi << 8) | hylo)
	if hytotal > 32768 :
		hytotal = hytotal - 65536 
        return hytotal

def GyroDataz():
        hzhi = bus.read_byte_data(0x6A, 0X2C)
        hzlo = bus.read_byte_data(0x6A, 0X2D)
        hztotal = ((hzhi << 8) | hzlo)
	if hztotal > 32768 :
		hztotal = hztotal - 65536 
        return hztotal

def GyroDataTotal():
        gtotal = (((GyroDatax()**2)+(GyroDatay()**2)+(GyroDataz()**2))**0.5)
        gtotal = (gtotal * 0.00875)
	return gtotal






bus.write_byte_data(0x1E,0x20,0x27) 
bus.write_byte_data(0x1E,0x23,0x40)
bus.write_byte_data(0x6A,0x20,0x0F)
bus.write_byte_data(0x6A,0x23,0x60)

while True:

	
	read1 = bus.read_byte_data(0x1e,0x0F)
	read2 = bus.read_byte_data(0x6a,0x0F)
	print read1
	print read2
    
        print "LSM330 Raw Data \nGyrotometer output: \nHx: ", GyroDatax()
        print "Hy: ", GyroDatay()
        print "Hz: ", GyroDataz()
	print "Gtotal: ",GyroDataTotal(), "dps""\n"
        print "\nAccelerometer output: \nax: ", accelDatax()
        print "ay: ", accelDatay()
        print "az: ", accelDataz()
	print "Atotal: ", accelDataTotal(),"g" "\n"
	
             
	time.sleep(.5)
