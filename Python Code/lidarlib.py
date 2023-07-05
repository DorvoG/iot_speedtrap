# Code Source: https://forums.raspberrypi.com/viewtopic.php?t=340841
from machine import UART, Pin
import utime
from binascii import hexlify


lidar = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5))    #Define receiving interface of Lidar 
'''
print(lidar)
utime.sleep_ms(1000)
'''
#"""
#byte[0] = 0x59
#byte[1] = 0x59
#byte[2] = Dist_L
#byte[3] = Dist_H
#byte[4] = Strength_L
#byte[5] = Strength_H
#byte[6] = Temp_L
#byte[7] = Temp_H
#byte[8] = Checksum
#total = byte[0]+byte[1]+byte[2]+byte[3]+byte[4]+byte[5]+byte[6]+byte[7]
#the lower 8 bits [LSB] of the total is the checksum 
#
#"""
frame_rate = 10 # default at 20Hz (best tested at 115200)

def save_settings():
    print("\nSaving setting...")
    info_packet = [0x5a,0x04,0x11,0x6F]
    lidar.write(bytes(info_packet))
    utime.sleep_ms(100)
    
def set_samp_rate(samp_rate=frame_rate):
    # change the sample rate
    global frame_rate
    print("Setting sample rate to {} Hz".format(samp_rate))
    samp_rate = int(samp_rate)
    frame_rate = samp_rate
    hex_rate = samp_rate.to_bytes(2,'big')
    print("hex_rate:{}".format(hex_rate)) # \xHH\xLL => hex_rate[0]=\xHH hex_rate[1]=\xLL 
    samp_rate_packet = [0x5a,0x06,0x03,hex_rate[1],hex_rate[0],00,00] # sample rate byte array
    for i in range(len(samp_rate_packet)):
        print(hex(samp_rate_packet[i]), end=" ")
    lidar.write(bytes(samp_rate_packet)) # send sample rate instruction
    utime.sleep(0.1) # wait for change to take effect
    save_settings()
    return

def get_version(UART1):
    # get version info | source: https://makersportal.com/blog/distance-detection-with-the-tf-luna-lidar-and-raspberry-pi
    info_packet = [0x5a,0x04,0x14,0x00]
    lidar.write(bytes(info_packet))
    start_tick = utime.time()
    while (utime.time()-start_tick < 10):
#         print('.',end = '')
#         utime.sleep_ms(1)
        bin_ascii = bytearray()
        if UART1.any() > 0:
            bin_ascii += UART1.read(30) # known 30 bytes-length response
            if bin_ascii[0] == 0x5a:
                hex_stream = hexlify(bin_ascii,' ').decode('utf-8')
                hex_array = hex_stream.split(" ")
                print(hex_stream) # uncomment this to see the HEX data
                print("{}".format(bin_ascii.decode('utf-8')))
                version = bin_ascii[0:].decode('utf-8')
                lst = []
                for c in version:
                    lst.append(c)
                
                for i in range(len(hex_array)):
                    print("0x{} : ascii -> {}".format(hex_array[i],lst[i]))
                print('\nVersion -'+version+'\n')
                return
            else:
                lidar.write(bytes(info_packet))
    print("Failed to retrieve version. This is a bit of a hit or miss kind of thing...")

def getLidarData(UART1):
    bin_ascii = bytearray()
    if UART1.any() > 0:
        bin_ascii += UART1.read(9) # byte [0-8] = 9 bytes
#         hex_stream = hexlify(bin_ascii,' ').decode()
#         print(hex_stream[0:26]) # uncomment this to see the HEX data

        if bin_ascii[0] == 0x59 and bin_ascii[1] == 0x59 :
            distance   = bin_ascii[2] + bin_ascii[3] * 256             #Get distance value  
            strength    = bin_ascii[4] + bin_ascii[5] * 256            #Get Strength value  
            temperature= (bin_ascii[6] + bin_ascii[7]* 256)/8-256      #Get IC temperature value
            #"""
            #bear in mind that serial printing at 20-30Hz drastically slowing down the entire process
            #please use other means of displaying the data using components such as:
            #i2c 16x2 LCD, i2c SSD1306 OLED, 7-segment TM1637, Dot Matrix MAX7219 
            #"""
            #print("D: {} cm S: {} T: {} *C\n".format(distance,strength,temperature))
            return (int(distance),int(strength),int(temperature))
'''
try:
    print("getting version")
    get_version(lidar)
    utime.sleep(1)
    # print("set sample rate via user input")
    # rate = input("Please enter 1-30 Hz for Raspi Pico:")
    # set_samp_rate(rate)
    #"""
    #TFmini-Plus readout on Raspberry Pi Pico does not work responsively
    #with frame rate set to anything higher than 30Hz at 115200 baud rate.
    
    #Generally:
    #1Hz-5Hz		usable for non-critical range sensing (slow response application)
    #6Hz-9Hz		good frame rate for semi-critical range sensing
    #10Hz-30Hz 	best for super critical range sensing

    #"""
    set_samp_rate(20) # min: 1 - max: 30 
    print("\nStart measuring")
    while True:
        getLidarData(lidar)
        
except KeyboardInterrupt:
    print("Program Stopped")
'''
