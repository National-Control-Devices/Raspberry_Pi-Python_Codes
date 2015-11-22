import time
import smbus
bus = smbus.SMBus(1)

C1 = 0
C2 = 0
C3 = 0
C4 = 0
C5 = 0
C6 = 0
D1 = 0.0
D2 = 0.0
Temp = 0.0 
Pres = 0.0



while True :
	
	C1 = bus.read_i2c_block_data(0x77, 0xA2,2) #Pressure Sensitivity
	C2 = bus.read_i2c_block_data(0x77, 0xA4,2) #Pressure Offset
	C3 = bus.read_i2c_block_data(0x77, 0xA6,2) #Temperature coefficient of Pressure sensitivity
	C4 = bus.read_i2c_block_data(0x77, 0xA8,2) #Temperature coefficient of Pressure offset
	C5 = bus.read_i2c_block_data(0x77, 0xAA,2) #Reference Temperature
	C6 = bus.read_i2c_block_data(0x77, 0xAC,2) #Temperature coefficient of the Temperature

	C1 = C1[0] * 256.0 + C1[1]
	C2 = C2[0] * 256.0 + C2[1]
	C3 = C3[0] * 256.0 + C3[1]
	C4 = C4[0] * 256.0 + C4[1]
	C5 = C5[0] * 256.0 + C5[1]
	C6 = C6[0] * 256.0 + C6[1]
	print "C1 :",C1
	print "C2 :",C2
	print "C3 :",C3
	print "C4 :",C4
	print "C5 :",C5
	print "C6 :",C6


	bus.write_byte(0x77,0x40)
	time.sleep(0.5)
	D1 = bus.read_i2c_block_data(0x77, 0x00,3)
	D1 = D1[0] * 65536 + D1[1] * 256.0 + D1[2]
	print"D1 :",D1
	
	bus.write_byte(0x77,0x50)
	time.sleep(0.5)
	D2 = bus.read_i2c_block_data(0x77, 0x00,3)
	D2 = D2[0] * 65536 + D2[1] * 256.0 + D2[2]
	print"D2 :",D2
	


	dT = D2 - (C5 * 2**8)
	Temp = 2000 + (dT * C6 / 2**23)
	print "dT :" ,dT
	OFF = C2 * 2**16 + (C4 * dT) / 2**7
	SENS = C1 * 2**15 + (C3 * dT) / 2**8

	if (Temp >= 2000):
		T2 = 0
		OFF2 = 0
		SENS2 = 0
	elif (Temp < 2000):
		T2 = dT * dT / 2**31
		OFF2 = 5 * ((Temp - 2000) ** 2) / 2
		SENS2 = OFF2 / 2
	elif (Temp < -1500):
		OFF2 = OFF2 + 7 * ((Temp + 1500) ** 2)
		SENS2 = SENS2 + 11 * (Temp + 1500) ** 2 / 2
	time.sleep(0.5) 

	Temp = Temp - T2
	OFF = OFF - OFF2
	SENS = SENS - SENS2

	Pres = (D1 * SENS / 2**21 - OFF) / 2**15
	Temp = Temp / 100 
	Pres = Pres / 10
	print "Temparature :" ,Temp, "C"
	print "Pressure    :" ,Pres, "mbar"
	

	














