import time
import smbus
bus = smbus.SMBus(1)

def setup():

	bus.write_byte_data(0x1E,0x00,0x10)
	bus.write_byte_data(0x1E,0x01,0x20)
	bus.write_byte_data(0x1E,0x02,0x00)
	
def reading():
      status = bus.read_byte_data(0x1E,0x09)
      time.sleep(0.5)
      read= bus.read_i2c_block_data(0x1E,0x03,6)
      X_Mag = read[0] +  (read[1] << 8)
  
      Y_Mag =  read[2] + (read[3] << 8)
       
      time.sleep(0.5)
      Z_Mag =  read[4] + (read[5]  << 8 )
            
      time.sleep(0.5)
      print 'XCompass' 
      print  X_Mag  * 0.00092 
      print 'YCompass'
      print  Y_Mag * 0.00092
      print 'ZCompass'  
      print  Z_Mag * 0.00092
      print status
      
setup()
    
while True:

    reading()