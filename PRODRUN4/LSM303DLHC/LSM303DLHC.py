import smbus
import time
import math

bus = smbus.SMBus(1)

def Write_Accl(register,value):
        bus.write_byte_data(0X19, register, value)
        return -1

def Write_Mag(register,value):
        bus.write_byte_data(0X1E, register, value)
        return -1

def Read_Accl(register):
        bus.read_byte_data(0X19, register)
        return -1

def Read_Mag(register):
        bus.read_byte_data(0X1E, register)
        return -1

def accelDatax():
        gxhi = bus.read_byte_data(0X19, 0X28)
        gxlo = bus.read_byte_data(0X19, 0X29)
        gxtotal = ((gxhi << 8) | gxlo)
        return gxtotal

def accelDatay():
        gyhi = bus.read_byte_data(0X19, 0X2A)
        gylo = bus.read_byte_data(0X19, 0X2B)
        gytotal = ((gyhi << 8) | gylo)
        return gytotal

def accelDataz():
        gzhi = bus.read_byte_data(0X19, 0X2C)
        gzlo = bus.read_byte_data(0X19, 0X2D)
        gztotal = ((gzhi << 8) | gzlo)
        return gztotal

def accelDataTotal():
        gtotal = (((accelDatax()**2)+(accelDatay()**2)+(accelDataz()**2))**0.5)
        gtotal = (gtotal / 32768)
	return gtotal

def magDatax():
        hxhi = bus.read_byte_data(0X1E, 0X03)
        hxlo = bus.read_byte_data(0X1E, 0X04)
        hxtotal = ((hxhi << 8) | hxlo)
        return hxtotal

def magDatay():
        hyhi = bus.read_byte_data(0X1E, 0X07)
        hylo = bus.read_byte_data(0X1E, 0X08)
        hytotal = ((hyhi << 8) | hylo)
        return hytotal

def magDataz():
        hzhi = bus.read_byte_data(0X1E, 0X05)
        hzlo = bus.read_byte_data(0X1E, 0X06)
        hztotal = ((hzhi << 8) | hzlo)
        return hztotal
        
def magDataTotal():
        htotal = (((magDatax()**2)+(magDatay()**2)+(magDataz()**2))**0.5)
        return htotal
        

Write_Accl(0X20, 0x27) 
Write_Accl(0X23, 0x40)

Write_Mag(0X02, 0x00) 

while True:
        print "LSM303DLHC Raw Data \nMagnetometer output: \nHx: ", magDatax()
        print "Hy: ", magDatay()
        print "Hz: ", magDataz()
        print math.degrees(math.atan(magDatay()/magDatax()))
	print "Htotal: ", magDataTotal(), "\n"
        print "\nAccelerometer output: \nGx: ", accelDatax()
        print "Gy: ", accelDatay()
        print "Gz: ", accelDataz()
        print "Gtotal: ", accelDataTotal(), "g" "\n"
        time.sleep(.5)
