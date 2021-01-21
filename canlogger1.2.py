#!/usr/bin/python3
# Third script, Parsing information and sending to Mqtt Broker

#Main import.
import paho.mqtt.client as paho #mqtt library
import sys
import glob
import time, datetime
import io
import os
import can

#MQTT settings
broker="127.0.0.1"
port=1883
ACCESS_TOKEN=''
#Defining publisher settings
publisher= paho.Client("canlogger")
publisher.connect(broker,port,keepalive=60)

#Some settings to make life easier.
SHOW_POWER_DATA = True
SHOW_BATTERY_DATA = True
SHOW_DCDC_DATA = True

#Get can0 up and running.
os.system("sudo /sbin/ip link set can0 up type can bitrate 500000 listen-only on")
time.sleep(0.1)
dev = can.interface.Bus(channel='can0', bustype='socketcan_native')
print("Waiting for CanBus traffic.")
#Main loop.
try:
    while True:
        message = dev.recv()
        if SHOW_BATTERY_DATA == True:
        #ID 102, Battery management system BMS.
            def batteryvoltage():
                return (message.data[1] * 256 + message.data[0]) / 100.
            def regencurrent():
                return (message.data[3] & 0x100000) * message.data[3] * 256 + message.data[2]
            def bmstemp():
                return ((message.data[6] + (message.data[7] & 0x07) << 8)) * 0.1
            if message.arbitration_id == 258:
                mqtt0 = publisher.publish(topic='batteryvoltage',payload=batteryvoltage())
                mqtt1 = publisher.publish(topic='regencurrent', payload=regencurrent())
                mqtt2 = publisher.publish(topic='bmstemp', payload=bmstemp())


            #ID 232, Power limits
            def maxdischargepower():
                return (message.data[2] + (message.data[3] << 8)) / 100.
            def maxregenpower():
                return (message.data[0] + (message.data[1] << 8)) / 100.
            if message.arbitration_id == 562:
                mqtt0 = publisher.publish(topic='maxdischargepower', payload=maxdischargepower())
                mqtt1 = publisher.publish(topic='maxregenpower', payload=maxregenpower())


            #ID 3D2, Total charge
            def kwhchargetotal():
                return (message.data[4] + (message.data[5] << 8) + (message.data[6] << 16) + (message.data[7] << 24)) / 1000.0
            def kwhdischargetotal():
                return (message.data[0] + (message.data[1] << 8) + (message.data[2] << 16) + (message.data[3] << 24)) / 1000.0
            if message.arbitration_id == 978:
                mqtt0 = publisher.publish(topic='kwhchargetotal', payload=kwhchargetotal())
                mqtt1 = publisher.publish(topic='kwhdischargetotal', payload=kwhdischargetotal())


            #ID 302 Battery Charge State
            def socmin():
                return (message.data[0] + ((message.data[1] & 0x3) << 8)) / 10.
            def socui():
                return ((message.data[1] >> 2) + ((message.data[2] & 0xf) << 6)) / 10.
            if message.arbitration_id == 770:
                mqtt0 = publisher.publish(topic='socmin', payload=socmin())
                mqtt1 = publisher.publish(topic='socui', payload=socui())


            #ID 382 Battery statistics
            def nominalFullPackEnergy():
                return (message.data[0] + ((message.data[1] & 0x3) << 8)) / 10.0
            def nominalEnergyRemaining():
                return ((message.data[1] >> 2) + ((message.data[2] & 0xf) * 64)) / 10.
            def expectedEnergyRemaining():
                return ((message.data[2] >> 4) + ((message.data[3] & 0x3f) * 16)) / 10.
            def idealEnergyRemaining():
                return ((message.data[3] >> 6) + ((message.data[4] & 0xff) * 4)) / 10.
            def energyBuffer():
                return ((message.data[6] >> 2) + ((message.data[7] & 0x03) * 64)) / 10.
            def energyToChargeComplete():
                return (message.data[5] + ((message.data[6] & 0x03) << 8)) / 10.
            if message.arbitration_id == 898:
                mqtt0 = publisher.publish(topic='nominalfullpackenergy', payload=nominalFullPackEnergy())
                mqtt1 = publisher.publish(topic='nominalenergyremaining', payload=nominalEnergyRemaining())
                mqtt2 = publisher.publish(topic='expectedenergyremaining', payload=expectedEnergyRemaining())
                mqtt3 = publisher.publish(topic='idealenergyremaining', payload=idealEnergyRemaining())
                mqtt4 = publisher.publish(topic='energybuffer', payload=energyBuffer())
                mqtt5 = publisher.publish(topic='energytochargecomplete', payload=energyToChargeComplete())



        if SHOW_POWER_DATA == True:
            #ID 106 Rear motor RPM
            def reardumotorrpm():
                return (message.data[4] + (message.data[5] << 8)) - (512 * (message.data[5] & 0x80))
            def reardupedalpos():
                return message.data[6] * 0.4
            if message.arbitration_id == 262:
                mqtt0 = publisher.publish(topic='reardumotorrpm', payload=reardumotorrpm())
                mqtt1 = publisher.publish(topic='reardupedalpos', payload=reardupedalpos())


            #ID 154 Rear DU more info
            def reardutorquemeassured():
                return (message.data[5] + ((message.data[6] & 0x1f) << 8) - (512 * (message.data[6] & 0x10))) / 4
            def reardupedalposa():
                return message.data[2] * 0.4
            def reardupedalposb():
                return message.data[3] * 0.4
            if message.arbitration_id == 340:
                mqtt0 = publisher.publish(topic='reardutorquemeassured', payload=reardutorquemeassured())
                mqtt1 = publisher.publish(topic='reardupedalposa', payload=reardupedalposa())
                mqtt2 = publisher.publish(topic='reardupedalposb', payload=reardupedalposb())


            #ID 266 Rear Du Power statistics.
            def rearinverter12V():
                return message.data[0] / 10.
            def reardudissipation():
                return message.data[1] * 125
            def reardudrivepowermax():
                return (((message.data[6] & 0x3F) << 5) + ((message.data[5] & 0xF0) >> 3)) + 1
            def reardumechpower():
                return ((message.data[2] + ((message.data[3] & 0x7) << 8)) - (512 * (message.data[3] & 0x4))) / 2.
            def reardustatorcurrent():
                return message.data[4] + ((message.data[5] & 0x7) << 8)
            def rearduregenpowermax():
                return (message.data[7] * 4) - 200
            if message.arbitration_id == 614:
                mqtt0 = publisher.publish(topic='rearinverter', payload=rearinverter12V())
                mqtt1 = publisher.publish(topic='reardudissipation', payload=reardudissipation())
                mqtt2 = publisher.publish(topic='reardudrivepowermax', payload=reardudrivepowermax())
                mqtt3 = publisher.publish(topic='reardumechpower', payload=reardumechpower())
                mqtt4 = publisher.publish(topic='reardustatorcurrent', payload=reardustatorcurrent())
                mqtt5 = publisher.publish(topic='rearduregenpowermax', payload=rearduregenpowermax())


            #ID 116 Rear DU Torque Status
            def reardugear():
                return (message.data[1] & 0x70) >> 4
            def reardugearrequest():
                return (message.data[3] & 0x70) >> 4
            def reardutorqueestimate():
                return ((message.data[0] + ((message.data[1] & 0xF) << 8)) - (512 * (message.data[1] & 0x8))) / 2
            def rearduvehiclespeed():
                return (((message.data[2] + ((message.data[3] & 0xf) << 8)) - 500) / 20)
            if message.arbitration_id == 278:
                mqtt0 = publisher.publish(topic='reardugear', payload=reardugear())
                mqtt1 = publisher.publish(topic='reardugearrequest', payload=reardugearrequest())
                mqtt2 = publisher.publish(topic='reardutorqueestimate', payload=reardutorqueestimate())
                mqtt3 = publisher.publish(topic='rearduvehiclespeed', payload=rearduvehiclespeed())

            #ID 1D4 Front Du Torque
            def frontdutorquemeassured():
                return ((message.data[0] + ((message.data[1] & 0xf) << 8)) - (512 * (message.data[1] & 0x8))) / 2.
            if message.arbitration_id == 468:
                mqtt0 = publisher.publish(topic='frontdutorquemeassured', payload=frontdutorquemeassured())


            #ID 2E5 Front Du Power statistics
            def frontinverter12V():
                return message.data[0] / 10.
            def frontdudissipation():
                return message.data[1] * 125
            def frontdudrivepowermax():
                return (((message.data[6] & 0x3F) << 5) + ((message.data[5] & 0xF0) >> 3)) + 1
            def frontdumechpower():
                return ((message.data[2] + ((message.data[3] & 0x7) << 8)) - (512 * (message.data[3] & 0x4))) / 2.
            def frontdustatorcurrent():
                return message.data[4] + ((message.data[5] & 0x7) << 8)
            if message.arbitration_id == 741:
                mqtt0 = publisher.publish(topic='frontinverter', payload=frontinverter12V())
                mqtt1 = publisher.publish(topic='frontdudissipation', payload=frontdudissipation())
                mqtt2 = publisher.publish(topic='frontdudrivepowermax', payload=frontdudrivepowermax())
                mqtt3 = publisher.publish(topic='frontdumechpower', payload=frontdumechpower())
                mqtt4 = publisher.publish(topic='frontdustatorcurrent', payload=frontdustatorcurrent())

            #ID 115 Front DU RPM
            def frontdumotorrpm():
                return (message.data[4] + (message.data[5] << 8)) - (512 * (message.data[5] & 0x80))
            if message.arbitration_id == 277:
                mqtt0 = publisher.publish(topic='frontdumotorrpm', payload=frontdumotorrpm())

            #ID 145
            def frontdutorqueestimate():
                return ((message.data[0] + ((message.data[1] & 0xf) << 8)) - (512 * (message.data[1] & 0x8))) / 2.
            if message.arbitration_id == 325:
                mqtt0 = publisher.publish(topic='frontdutorqueestimate', payload=frontdutorqueestimate())


        if SHOW_DCDC_DATA == True:
            #ID 210 DC DC statistics
            def inlettemperature():
                return ((message.data[2] - (2 * (message.data[2] & 0x80))) / 2) + 40
            def inputpower():
                return message.data[3] * 16
            def outputcurrent():
                return message.data[4]
            def outputpower():
                return message.data[4] * (message.data[5] / 10.)
            def outputvoltage():
                return message.data[5] / 10
            if message.arbitration_id == 528:
                mqtt0 = publisher.publish(topic='inlettemperature', payload=inlettemperature())
                mqtt1 = publisher.publish(topic='inputpower', payload=inputpower())
                mqtt2 = publisher.publish(topic='outputcurrent', payload=outputcurrent())
                mqtt3 = publisher.publish(topic='outputpower', payload=outputpower())
                mqtt4 = publisher.publish(topic='outputvoltage', payload=outputvoltage())




# Ctrl-C Keyboard exit.
except KeyboardInterrupt:
    # Catch keyboard interrupt
    os.system("sudo /sbin/ip link set can0 down")
    print('\n\rKeyboard interrtupt')

#End of script.


