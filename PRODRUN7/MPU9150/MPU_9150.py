import smbus
import time
import math

bus = smbus.SMBus(1)

def Write_Accl(register,value):
        bus.write_byte_data(0x68, register, value)
        return -1

def Write_Gyro(register,value):
        bus.write_byte_data(0x68, register, value)
        return -1

def writeMag(register,value):
        bus.write_byte_data(0x0C, register, value)
        return -1

def readAcclx():
        axhi = bus.read_byte_data(0x68, 0X3B)
        axlo = bus.read_byte_data(0x68, 0X3C)
        axtotal = ((axhi << 8) | axlo)
	if axtotal > 32768 :
		axtotal = axtotal - 65536
        return axtotal

def readAccly():
        ayhi = bus.read_byte_data(0x68, 0X3D)
        aylo = bus.read_byte_data(0x68, 0X3E)
        aytotal = ((ayhi << 8) | aylo)
	if aytotal > 32768 :
		aytotal = aytotal - 65536 
        return aytotal

def readAcclz():
        azhi = bus.read_byte_data(0x68, 0X3F)
        azlo = bus.read_byte_data(0x68, 0X40)
        aztotal = ((azhi << 8) | azlo)
	if aztotal > 32768 :
		aztotal = aztotal - 65536 
        return aztotal


def accelDataTotal():
        atotal = (((readAcclx()**2)+(readAccly()**2)+(readAcclz()**2))**0.5)
        atotal = (atotal / 32768)
	return atotal



def readGYRx():
        hxhi = bus.read_byte_data(0x68, 0X43)
        hxlo = bus.read_byte_data(0x68, 0X44)
        hxtotal = ((hxhi << 8) | hxlo)
	if hxtotal > 32768 :
		hxtotal = hxtotal - 65536 
        return hxtotal

def readGYRy():
        hyhi = bus.read_byte_data(0x68, 0X45)
        hylo = bus.read_byte_data(0x68, 0X46)
        hytotal = ((hyhi << 8) | hylo)
	if hytotal > 32768 :
		hytotal = hytotal - 65536
        return hytotal

def readGYRz():	
        hzhi = bus.read_byte_data(0x68, 0X47)
        hzlo = bus.read_byte_data(0x68, 0X48)
        hztotal = ((hzhi << 8) | hzlo)
	if hztotal > 32768 :
		hztotal = hztotal - 65536
        return hztotal


def GyroDataTotal():
        gtotal = (((readGYRx()**2)+(readGYRy()**2)+(readGYRz()**2))**0.5)
        gtotal = (gtotal * 245 / 32768)
	return gtotal


def readMagx():
        Mag_l = bus.read_byte_data(0x0C,0x03)
        Mag_h = bus.read_byte_data(0x0C,0x04)
        Mag_total = (Mag_l | Mag_h <<8)
        return Mag_total  if Mag_total < 32768 else Mag_total - 65536


def readMagy():
        Mag_l = bus.read_byte_data(0x0C,0x05)
        Mag_h = bus.read_byte_data(0x0C,0x06)
        Mag_total = (Mag_l | Mag_h <<8)
        return Mag_total  if Mag_total < 32768 else Mag_total - 65536


def readMagz():
        Mag_l = bus.read_byte_data(0x0C,0x07)
        Mag_h = bus.read_byte_data(0x0C,0x08)
        Mag_total = (Mag_l | Mag_h <<8)
        return Mag_total  if Mag_total < 32768 else Mag_total - 65536


def MagDataTotal():
        mtotal = (((readMagx()**2)+(readMagy()**2)+(readMagz()**2))**0.5)
        mtotal = (mtotal *0.3)
	return mtotal
 

while True:
	     
	
	bus.write_byte_data(0x68,0x6B,0x00)
	bus.write_byte_data(0x0C,0x0A,0x01)
	
	#Read our Acclelerometer,gyroscope and Magnetometer  values
	Acclx = readAcclx()
	Accly = readAccly()
	Acclz = readAcclz()
	GYRx = readGYRx()
	GYRy = readGYRx()
	GYRz = readGYRx()
	Magx = readMagx()
	Magy = readMagy()
	Magz = readMagz()
	
	##Convert Acclelerometer values to print "Mtotal       : " ,MagDataTotal(),"Guass"degrees
	AcclXangle =  (math.atan2(Accly,Acclz)+3.14)*57.3
	AcclYangle =  (math.atan2(Acclz,Acclx)+3.14)*57.3


        #If IMU is up the correct way, use these lines
        AcclXangle -= 180.0
	if AcclYangle > 90:
	        AcclYangle -= 270.0
	else:
		AcclYangle += 90.0
	
	#Calculate heading
	heading = 180 * math.atan2(Magy,Magx)/3.14

	if heading < 0:
	 	heading += 360


	#Normalize Acclelerometer raw values.
        AcclXnorm = Acclx/math.sqrt(Acclx * Acclx + Accly * Accly + Acclz * Acclz)
	AcclYnorm = Accly/math.sqrt(Acclx * Acclx + Accly * Accly + Acclz * Acclz)



	#Calculate pitch and roll
	pitch = math.asin(AcclXnorm)
	roll = -math.asin(AcclYnorm/math.cos(pitch))

	#Calculate the new tilt compensated values
	MagXcomp = Magx*math.cos(pitch)+Magz*math.sin(pitch)
	MagYcomp = Magx*math.sin(roll)*math.sin(pitch)+Magy*math.cos(roll)-Magz*math.sin(roll)*math.cos(pitch)


        print " Raw Data \nGyrometer output: \nHx: ", readGYRx()
        print "Hy: ", readGYRy()
        print "Hz: ", readGYRz()
	print "Gtotal: ",GyroDataTotal(), "dps""\n"
	print "\nAccelerometer output: \nGx: ", readAcclx()
        print "Gy: ", readAccly()
        print "Gz: ", readAcclz()
	print "AcclX Anglen : " ,AcclXangle
	print "AcclY Angle  : " ,AcclYangle
	print "Atotal: ", accelDataTotal(),"g" "\n"
	print "\nMagnetometer  output:"
	print "Mx: ", readMagx()
	print "My: ", readMagy()
	print "Mz: ", readMagz()
	print "Mtotal       :: " ,MagDataTotal(),"microT"
	print "HEADING      : " ,heading
	print "MagX component  Tilt:",MagXcomp
	print "MagY component Tilt :",MagYcomp
	print "****************************"
	
	
        time.sleep(.5)
