import lidarlib
import conf
import utime

from servolib import Servo
sg90_servo = Servo(pin=6)
sg90_servo.move(6)

from machine import UART, Pin
lidar = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5))    #Define receiving interface of Lidar 

class measure_speed:
    
    def measure_lidar(self, dir):
        try:
            
            lidarlib.set_samp_rate(conf.lidar_refreshrate) # min: 1 - max: 30 
            print("\nStart measuring")
            
            # implementing a timer to prevent the pico from getting stuck in the measureloop and running out of RAM
            end_time = utime.time() + 10
            
            speed_list = []
            
            while True:
                data = lidarlib.getLidarData(lidar)
                if (data != None):
                    speed_list.append(data)
                    break
            
#            print(speed_list[0][0]) # Implemented for debugging
            
            while True:
                while True:
                    data = lidarlib.getLidarData(lidar)
                    if (data != None):
                        speed_list.append(data)
                        break
                    
                speed = int(abs((speed_list[-1][0] - speed_list[-2][0]) /  (1 / conf.lidar_refreshrate))) # divide by update frequency
                speed_kmh = speed  / 100 * 3.6 #divide by meters and then multiply for km/h
                
                # Prevent the servo from moving where it's not supposed to
                if (speed_kmh > 60): 
                    speed_kmh = 60
                sg90_servo.move(6 + 2 * speed_kmh)
                
                # If timer is reached without other breaks triggered then break out of the loop
                if (utime.time() > end_time):
                    break
                
                
        except KeyboardInterrupt:
            print("Program Stopped")
        
        # return servo to hold position
        sg90_servo.move(6)
        
#        print("stop") # Debugging print
        return speed_list

