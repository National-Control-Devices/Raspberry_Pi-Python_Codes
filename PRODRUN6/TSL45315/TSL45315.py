import smbus
import time 
bus = smbus.SMBus(1)

def enableMeasurement():
        bus.write_byte_data(0x29,0x80,0x03)

def disableMeasurement():
        bus.write_byte_data(0x29,0x80,0x00)

def getLux():
        data_bytes = bus.read_i2c_block_data(0x29, 0x04 | 0x80, 2)
        data = (data_bytes[1] << 8 | data_bytes[0])
	time.sleep(0.2)
	return data

enableMeasurement()

while True:

    lux = getLux()
    print "   light = %dlux" % ( lux )