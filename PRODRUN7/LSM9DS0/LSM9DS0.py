import smbus
import time
import math

bus = smbus.SMBus(1)



def writeAccl(register,value):
        bus.write_byte_data(0x1E , register, value)
        return -1

def writeMag(register,value):
        bus.write_byte_data(0x1E, register, value)
        return -1

def writeGyro(register,value):
        bus.write_byte_data(0x6A, register, value)
        return -1



def readAcclx():
        Accl_l = bus.read_byte_data(0x1E,0x28)
        Accl_h = bus.read_byte_data(0x1E,0x29)
	Accl_total = (Accl_l | Accl_h <<8)
	return Accl_total  if Accl_total < 32768 else Accl_total - 65536


def readAccly():
        Accl_l = bus.read_byte_data(0x1E,0x2A)
        Accl_h = bus.read_byte_data(0x1E,0x2B)
	Accl_total = (Accl_l | Accl_h <<8)
	return Accl_total  if Accl_total < 32768 else Accl_total - 65536


def readAcclz():
        Accl_l = bus.read_byte_data(0x1E,0x2C)
        Accl_h = bus.read_byte_data(0x1E,0x2D)
	Accl_total = (Accl_l | Accl_h <<8)
	return Accl_total  if Accl_total < 32768 else Accl_total - 65536

def accelDataTotal():
        atotal = (((readAcclx()**2)+(readAccly()**2)+(readAcclz()**2))**0.5)
        atotal = (atotal * 0.732 ) / 1000
	return atotal


def readMagx():
        Mag_l = bus.read_byte_data(0x1E,0x08)
        Mag_h = bus.read_byte_data(0x1E,0x09)
        Mag_total = (Mag_l | Mag_h <<8)
        return Mag_total  if Mag_total < 32768 else Mag_total - 65536


def readMagy():
        Mag_l = bus.read_byte_data(0x1E,0x0A)
        Mag_h = bus.read_byte_data(0x1E,0x0B)
        Mag_total = (Mag_l | Mag_h <<8)
        return Mag_total  if Mag_total < 32768 else Mag_total - 65536


def readMagz():
        Mag_l = bus.read_byte_data(0x1E,0x0C)
        Mag_h = bus.read_byte_data(0x1E,0x0D)
        Mag_total = (Mag_l | Mag_h <<8)
        return Mag_total  if Mag_total < 32768 else Mag_total - 65536


def MagDataTotal():
        mtotal = (((readMagx()**2)+(readMagy()**2)+(readMagz()**2))**0.5)
        mtotal = (mtotal * 0.48 ) / 1000
	return mtotal


def readGYRx():
        gyr_l = bus.read_byte_data(0x6A,0x28)
        gyr_h = bus.read_byte_data(0x6A,0x29)
        gyr_total = (gyr_l | gyr_h <<8)
        return gyr_total  if gyr_total < 32768 else gyr_total - 65536
  

def readGYRy():
        gyr_l = bus.read_byte_data(0x6A,0x2A)
        gyr_h = bus.read_byte_data(0x6A,0x2B)
        gyr_total = (gyr_l | gyr_h <<8)
        return gyr_total  if gyr_total < 32768 else gyr_total - 65536

def readGYRz():
        gyr_l = bus.read_byte_data(0x6A,0x2C)
        gyr_h = bus.read_byte_data(0x6A,0x2D)
        gyr_total = (gyr_l | gyr_h <<8)
        return gyr_total  if gyr_total < 32768 else gyr_total - 65536

#initialise the Acclelerometer
writeAccl(0x20,0x67) #z,y,x axis enabled, continuos update,  100Hz data rate
writeAccl(0x21,0x20) #+/- 16G full scale

#initialise the Magnetometer
writeMag(0x24,0xF0) #Temp enable, M data rate = 50Hz
writeMag(0x25,0x60) #+/-12gauss
writeMag(0x26,0x00) #Continuous-conversion mode

#initialise the gyroscope
writeGyro(0x20,0x0F) #Normal power mode, all axes enabled
writeGyro(0x23,0x30) #Continuos update, 2000 dps full scale


gyroXangle = 0.0
gyroYangle = 0.0
gyroZangle = 0.0

while True:
	
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

	##Convert Acclelerometer values to degrees
	AcclXangle =  (math.atan2(Accly,Acclz)+3.14)*57.3
	AcclYangle =  (math.atan2(Acclz,Acclx)+3.14)*57.3

	#Convert Gyro raw to degrees per second
	rate_gyr_x =  GYRx * 0.070
	rate_gyr_y =  GYRy * 0.070
	rate_gyr_z =  GYRz * 0.070

	#Calculate the angles from the gyro. 0.041 = loop period 
	gyroXangle+=rate_gyr_x*0.041
	gyroYangle+=rate_gyr_y*0.041
	gyroZangle+=rate_gyr_z*0.041


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

	print "Atotal       : " ,accelDataTotal(),"g" 
	print "Mtotal       : " ,MagDataTotal(),"Guass"
 	print "AcclX Anglen : " ,AcclXangle
	print "AcclY Angle  : " ,AcclYangle
	print "GyroX Angle  : " ,gyroXangle
	print "GYRY Angle   : " ,gyroYangle
	print "GYRZ Angle   : " ,gyroZangle
	print "HEADING      : " ,heading
	print "MagX component  Tilt:",MagXcomp
	print "MagY component Tilt :",MagYcomp
	print "****************************"
        time.sleep(0.5)
	
