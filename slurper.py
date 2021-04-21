# Slurper that logs all known ArbitrationID's to textfiles.

#Main import.
import sys
import glob
import time, datetime
import io
import os
import can
import csv


#Some settings to make life easier.

SHOW_BATTERY_DATA = True


#Get can0 up and running.
os.system("sudo /sbin/ip link set can0 up type can bitrate 500000 listen-only on")
time.sleep(0.1)
os.system("sudo /sbin/ifconfig lo add 42.42.42.42")
dev = can.interface.Bus(channel='can0', bustype='socketcan_native')
#Main loop.

#Create all the csv files




try:
    while True:
        message = dev.recv()
        if SHOW_BATTERY_DATA == True:

            # ID 14, Battery management system BMS.
            if message.arbitration_id == 14:
                file = open("14.txt", "a")
            file.write(str(message) + "\n")
            file.close()

            # ID 258, Battery management system BMS.
            if message.arbitration_id == 258:
                file = open("258.txt", "a")
            file.write(str(message) + "\n")
            file.close()

            # ID 262, Battery management system BMS.
            if message.arbitration_id == 262:
                file = open("262.txt", "a")
            file.write(str(message) + "\n")
            file.close()

            # ID 277, Battery management system BMS.
            if message.arbitration_id == 277:
                file = open("277.txt", "a")
            file.write(str(message) + "\n")
            file.close()

            # ID 278, Battery management system BMS.
            if message.arbitration_id == 278:
                file = open("278.txt", "a")
            file.write(str(message) + "\n")
            file.close()

            # ID 325, Battery management system BMS.
            if message.arbitration_id == 325:
                file = open("325.txt", "a")
            file.write(str(message) + "\n")
            file.close()

            # ID 340, Battery management system BMS.
            if message.arbitration_id == 340:
                file = open("340.txt", "a")
            file.write(str(message) + "\n")
            file.close()

            # ID 360, Battery management system BMS.
            if message.arbitration_id == 360:
                file = open("360.txt", "a")
            file.write(str(message) + "\n")
            file.close()

            # ID 468, Battery management system BMS.
            if message.arbitration_id == 468:
                file = open("468.txt", "a")
            file.write(str(message) + "\n")
            file.close()

            # ID 528, Battery management system BMS.
            if message.arbitration_id == 528:
                file = open("528.txt", "a")
            file.write(str(message) + "\n")
            file.close()

            # ID 562, Battery management system BMS.
            if message.arbitration_id == 562:
                file = open("562.txt", "a")
            file.write(str(message) + "\n")
            file.close()

            # ID 614, Battery management system BMS.
            if message.arbitration_id == 614:
                file = open("614.txt", "a")
            file.write(str(message) + "\n")
            file.close()

            # ID 648, Battery management system BMS.
            if message.arbitration_id == 648:
                file = open("648.txt", "a")
            file.write(str(message) + "\n")
            file.close()

            # ID 680, Battery management system BMS.
            if message.arbitration_id == 680:
                file = open("680.txt", "a")
            file.write(str(message) + "\n")
            file.close()

            # ID 682, Battery management system BMS.
            if message.arbitration_id == 682:
                file = open("682.txt", "a")
            file.write(str(message) + "\n")
            file.close()

            # ID 741, Battery management system BMS.
            if message.arbitration_id == 741:
                file = open("741.txt", "a")
            file.write(str(message) + "\n")
            file.close()

            # ID 770, Battery management system BMS.
            if message.arbitration_id == 770:
                file = open("770.txt", "a")
            file.write(str(message) + "\n")
            file.close()

            # ID 774, Battery management system BMS.
            if message.arbitration_id == 774:
                file = open("774.txt", "a")
            file.write(str(message) + "\n")
            file.close()

            # ID 776, Battery management system BMS.
            if message.arbitration_id == 776:
                file = open("776.txt", "a")
            file.write(str(message) + "\n")
            file.close()

            # ID 792, Battery management system BMS.
            if message.arbitration_id == 792:
                file = open("792.txt", "a")
            file.write(str(message) + "\n")
            file.close()

            # ID 794, Battery management system BMS.
            if message.arbitration_id == 794:
                file = open("794.txt", "a")
            file.write(str(message) + "\n")
            file.close()

            # ID 824, Battery management system BMS.
            if message.arbitration_id == 824:
                file = open("824.txt", "a")
            file.write(str(message) + "\n")
            file.close()

            # ID 898, Battery management system BMS.
            if message.arbitration_id == 898:
                file = open("898.txt", "a")
            file.write(str(message) + "\n")
            file.close()

            # ID 904, Battery management system BMS.
            if message.arbitration_id == 904:
                file = open("904.txt", "a")
            file.write(str(message) + "\n")
            file.close()

            # ID 978, Battery management system BMS.
            if message.arbitration_id == 978:
                file = open("978.txt", "a")
            file.write(str(message) + "\n")
            file.close()

            # ID 1016, Battery management system BMS.
            if message.arbitration_id == 1016:
                file = open("1016.txt", "a")
            file.write(str(message) + "\n")
            file.close()

            # ID 1378, Battery management system BMS.
            if message.arbitration_id == 1378:
                file = open("1378.txt", "a")
            file.write(str(message) + "\n")
            file.close()

            # ID 1778, Battery management system BMS.
            if message.arbitration_id == 1778:
                file = open("1778.txt", "a")
            file.write(str(message) + "\n")
            file.close()
# Ctrl-C Keyboard exit.
except KeyboardInterrupt:
    # Catch keyboard interrupt
    os.system("sudo /sbin/ip link set can0 down")



#End of script.
