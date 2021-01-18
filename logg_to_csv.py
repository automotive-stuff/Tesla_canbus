#!/usr/bin/python3
# First script, logging to a file.

#Main import.
import sys
import glob
import time, datetime
import io
import os
import can

#Some settings to make life easier.
SHOW_ALL_IDs = False
WRITE_TO_FILE = True
SHOW_POWER_DATA = True
SHOW_BATT_DATA = True
LOGGING_ENABLED = False
FILE_NAME = '' #Defaults to current date and time

#Global Variables
frame_counter = 0
MAX_NUMBER_OF_FRAMES = 20000

#Get can0 up and running.
os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")
dev = can.interface.Bus(channel='can0', bustype='socketcan_native')

#If logging True then log to x file.
if WRITE_TO_FILE == True:
  if FILE_NAME != '':
      st = FILE_NAME
  else:
      st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H.%M.%S')
  file_ = open('/home/pi/CANBUS/seperate/log/' + st + '.csv', 'w')
  print('New File Opened, now logging data. ')

#Goes through the ammount of frames defined above, for testing purpose.
while frame_counter <= MAX_NUMBER_OF_FRAMES:
    frame_counter = frame_counter + 1
    message = dev.recv()

    #Battery modeule data
    if SHOW_BATT_DATA == True:
        
        #ID 302 SOC UI
        if message.arbitration_id == 770:
            soc_ui = ((message.data[1]>>2) + ((message.data[2] & 0xF)<<6)) / 10
        #ID 102 BatteryPower kW
        if message.arbitration_id == 258:
            pack_volt = (message.data[0] | (message.data[1]<<8))/100
            #pack_current = (((message.data[2] | (message.data[3]<<8)) - ((message.data[2] | (message.data[3]<<8)) & 0x8000))-10000)/10
            pack_current = (((message.data[2] + ((message.data[3] & 0x3F)<<8)) - ((message.data[3] & 0x40)<<8))-10000)/10
        #ID 6F2 Cell Temp Average
        if message.arbitration_id == 1778 and message.data[0] > 23:
            d1 = (message.data[1] | ((message.data[2] & 0x03F)<<8))
            pack_temp = (d1 * 0.0122)

    if SHOW_POWER_DATA == True:
        #ID 266 Power dissipation, Shaftpower, StatorCurrent In Kw
        if message.arbitration_id == 614:
            pDiss = message.data[1] * 125
            mechPower = ((message.data[2] + ((message.data[3] & 0x7)<<8))-(512 * (message.data[3] & 0x4))) / 2
            statorCurr = message.data[4] + ((message.data[5] & 0x7)<<8)
        #ID 154 Rear Drive unit Torque in Nm and pedalpos in %
        if message.arbitration_id == 340:
            rtorqMeas = (message.data[5] + ((message.data[6] & 0x1F)<<8)-(512 * (message.data[6] & 0x10))) * 0.25
            pedalPos = (message.data[2] * 0.4)
        #ID 145 Front Drive unit Torque in Nm
        if message.arbitration_id == 325:
            ftorqMeas = (message.data[5] + ((message.data[6] & 0x1F) << 8) - (512 * (message.data[6] & 0x10))) * 0.25
        #ID116 Speed
        if message.arbitration_id == 278:
            speedKMH = ((message.data[2] + ((message.data[3] & 0xF)<<8))-500) / 20
            torqEst = ((message.data[0] + ((message.data[1] & 0xF)<<8))-(512 * (message.data[1] & 0x8))) / 2
        #ID106 Rear motor RPM
        if message.arbitration_id == 262:
            rmtrRPM = (message.data[4] + (message.data[5]<<8))-(512 * (message.data[5]&0x80))
        #ID115 Front motor RPM
        if message.arbitration_id == 277:
            fmtrRPM = (message.data[4] + (message.data[5] << 8)) - (512 * (message.data[5]&0x80))

    if WRITE_TO_FILE == True:
        if frame_counter == 1:
            write_data = ("time, msg_id, soc, temp, pedal_pos, pack_volt, pack_current, torque, mechPower, speedKMH, RmotorRPM, FmotorRPM\n")
        else:
            write_data = ("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (time.time(), hex(message.arbitration_id)[2:], soc_ui, pack_temp, pedalPos, pack_volt, pack_current, rtorqMeas, ftorqMeas, mechPower, speedKMH, rmtrRPM, fmtrRPM))
        file_.write(write_data)
        
if WRITE_TO_FILE == True:
  file_.close()
  print("File " + st + '.csv closed. ')

os.system("sudo /sbin/ip link set can0 down")
print("Connection Closed")
