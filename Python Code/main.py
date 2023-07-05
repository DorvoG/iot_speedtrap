import lidarlib
import event
import measure
import conf

import struct
import binascii
import utime

print("Main")

# Initialize measure-function
speed_test = measure.measure_speed()

# Main loop of program
while True:
    pir1_state = pir1.value()
    pir2_state = pir2.value()
 #   start = input()
  #  if (start == "banana"):
  #      speed_test.measure_lidar(None)
    if (pir1_state):
        speed_list = speed_test.measure_lidar(None)
        
        # Extract the 0th element from each tuple in the list
        speed_values = [item[0] for item in speed_list]
        
        # To find the highest value
        highest = int(max(speed_values))
        
        # To calculate the mean
        mean = int(sum(speed_values) / len(speed_values))
        
        payload = struct.pack(">hH", highest, mean)
        payload = binascii.hexlify(payload).decode("utf-8")
        
    
        lora.sendMsg(payload)
        print("Sent message:", payload)

        response = lora.receiveMsg()

        if (response != ""):
            print("Received: ", end=": ")
            print(response)
        speed_list = []
        speed_values = []

    if (pir2_state):
        speed_list = speed_test.measure_lidar(None)
        
        # Extract the 0th element from each tuple in the list
        speed_values = [item[0] for item in speed_list]
        
        # To find the highest value
        highest = int(max(speed_values))
        
        # To calculate the mean
        mean = int(sum(speed_values) / len(speed_values))
        
        payload = struct.pack(">hH", highest, mean)
        payload = binascii.hexlify(payload).decode("utf-8")
        
        lora.sendMsg(payload)
        print("Sent message:", payload)

        response = lora.receiveMsg()

        if (response != ""):
            print("Received: ", end=": ")
            print(response)
        speed_list = []
        speed_values = []
        
print("Main")
