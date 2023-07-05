#placeholder
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
            
            end_time = utime.time() + 10
            
            speed_list = []
            
            while True:
                data = lidarlib.getLidarData(lidar)
                if (data != None):
                    speed_list.append(data)
                    break
            
            time1 = utime.ticks_us()
            print(speed_list[0][0])
            
            while True:
                while True:
                    data = lidarlib.getLidarData(lidar)
                    if (data != None):
                        speed_list.append(data)
                        break
                    
                time2 = utime.ticks_us()
                speed = int(abs((speed_list[-1][0] - speed_list[-2][0]) /  (1 / conf.lidar_refreshrate))) # divide by update frequency
                speed_kmh = speed  / 100 * 3.6 #divide by meters and then multiply for km/h
                time1 = utime.ticks_us()
                
                if (speed_kmh > 60): 
                    speed_kmh = 60
                sg90_servo.move(6 + 2 * speed_kmh)
                
                if (utime.time() > end_time):
                    break
                
                
        except KeyboardInterrupt:
            print("Program Stopped")
        
        sg90_servo.move(6)
        print("stop")
        return speed_list

