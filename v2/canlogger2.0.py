#!/usr/bin/python3
# WORK IN PROGRESS NOT COMPLETE!

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

#VARIABLES
miles_to_km = 1.609344
kw_to_hp = 1.34102209
#Some settings to make life easier.
SHOW_POWER_DATA = True
SHOW_BATTERY_DATA = True
SHOW_DCDC_DATA = True

#Get can0 up and running.
os.system("sudo /sbin/ip link set can0 up type can bitrate 500000 listen-only on")
time.sleep(0.1)
os.system("sudo /sbin/ifconfig lo add 42.42.42.42")
dev = can.interface.Bus(channel='can0', bustype='socketcan_native')
try:
    while True:
        message = dev.recv()
        def steeringangle():
            return (((message.data[0] << 8) + message.data[1] - 8200.0) / 10.0)
        if message.arbitration_id == 14:
            mqtt0 = publisher.publish(topic='Steeringangle', payload=steeringangle())
        ##########################
        ###-258-102-batteryvoltage
        ##09 85 ba ff c0 ff fc 1f
        ##fb 84 bd ff ad ff fc 1f
        ##########################

        def batteryvoltage():
            return (message.data[1] * 256 + message.data[0]) / 100.
        def batterycurrent():
            return (message.data[3] & 0x100000) * message.data[3] * 256 + message.data[2]
        def batterypower():
            return batterycurrent() * batteryvoltage() / 1000.0

        ##########################
        ###-262-106-rr-motor-rpm
        ##00 20 00 80 00 00 00 a7
        ##90 60 8c 80 13 00 20 36
        ##########################

        def rrmotorrpm():
            return (message.data[4] + (message.data[5] << 8)) - (512 * (message.data[5] & 0x80))

        if message.arbitration_id == 262:
            mqtt0 = publisher.publish(topic='RMotorRPM', payload=rrmotorrpm())
        ##########################
        ###-277-115-fr-motor-rpm
        ##00 e0 00 80 00 00 76
        ##99 a0 96 80 23 00 88
        ##########################

        def frmotorrpm():
            return (message.data[4] + (message.data[5] << 8)) - (512 * (message.data[5] & 0x80))
        if message.arbitration_id == 277:
            mqtt0 = publisher.publish(topic='FMotorRPM', payload=frmotorrpm())
        ##########################
        ###-278-116-rr-torque-estimate
        ##ff 1f f4 11 8b c5
        ##65 40 00 42 8b 89
        ##########################
        #tvasjuatta = ([0x65, 0x40, 0x00, 0x42, 0x8b, 0x89])

        def rrtorqueestimate():
            return ((message.data[0] + ((message.data[1] & 0xF) << 8)) - (512 * (tvasjuatta[1] & 0x8))) / 2
        def speed():
            return ((message.data[2] + ((message.data[3] & 0xF) << 8)) - 500) / 20.0 * miles_to_km
        def consumption():
            return batterypower() / speed() * 1000
        if message.arbitration_id == 278:
            mqtt0 = publisher.publish(topic='Speed', payload=speed())


        ##########################
        ###-325-145-fr-torque-estimate
        ##ff cf 14
        ##60 e0 86
        ##########################

        def frtorqueestimate():
            return ((message.data[0] + ((message.data[1] & 0xF) << 8)) - (512 * (message.data[1] & 0x8))) / 2

        ##########################
        ###-340-154-watt-pedal
        ##18 32 10 00 00 ff 3f ed
        ##18 b2 10 20 1d 92 40 3e
        ##########################

        def rrtorquemeasured():
            return (message.data[5] + ((message.data[6] & 0x1F) << 8) - (512 * (message.data[6] & 0x10))) * 0.25
        def wattpedal():
            return message.data[3] * 0.4


        if message.arbitration_id == 340:
            mqtt0 = publisher.publish(topic='WattPedal', payload=wattpedal())

        ##########################
        ###-468-1D4-fr-torque_torquebias
        ##00 04 00 00 08 7f 60 c0
        ##00 04 00 00 08 b4 3f d4
        ##########################
        def frtorquemeasured():
            return (message.data[5] + ((message.data[6] & 0x1F) << 8) - (512 * (message.data[6] & 0x10))) * 0.25
        def rrtorquelol():
            return 0
        #def rrfrtorquebias():
         #   return 0 if frtorquemeasured() > rrtorquemeasured() == 1 else frtorquemeasured() / (rrtorquemeasured() + rrtorquemeasured()) * 100


        #if message.arbitration_id == 468:
         #   mqtt0 = publisher.publish(topic='TorqueBias', payload=rrfrtorquebias())
        ##########################
        ###-528-210-dc-dc
        ##00 00 cc 17 18 89 00
        ##00 00 ca 1b 1e 89 00
        ##########################
        def dcdccurrent():
            return message.data[4]
        def dcdcvoltage():
            return message.data[5] / 10.0
        def dcdccoolantinlet():
            return ((message.data[2] - (2 * (message.data[2] & 0x80))) * 0.5) + 40
        def dcdcinputpower():
            return (message.data[3] * 16)
        def twelvevoltsystem():
            return (message.data[3] * 16)
        def dcdcoutputpower():
            return (message.data[4] * message.data[5] / 10.0)
        def dcdcefficiency():
            return dcdcoutputpower() / dcdcinputpower() * 100.0
        def fourhundredvoltsystem():
            return batterypower() - dcdcinputpower() / 1000.0

        ##########################
        ###-562-232-max-discharge
        ##51 08 f0 7e
        ##4c 08 e6 7e
        ##########################
        def maxbmsdischarge():
            return (message.data[2] + (message.data[3] << 8)) / 100.0
        def maxbmscharge():
            return (message.data[0] + (message.data[1] << 8)) / 100.0

        ##########################
        ###-614-266-rr-dissipation
        ##87 02 00 00 00 28 4a 38
        ##87 02 09 00 80 28 0a 38
        ##########################
        def rrinvertertwelvevolt():
            return message.data[0] / 10.0
        def rrmechpower():
            return ((message.data[2] + ((message.data[3] & 0x7) << 8)) - (512 * (message.data[3] & 0x4))) / 2.0
        def rrdissipation():
            return message.data[1] * 125.0 / 1000.0 - 0.5
        def rrinputpower():
            return rrmechpower() + rrdissipation()
        def rrmechpowerhp():
            return rrmechpower() * kw_to_hp
        def rrstatorcurrent():
            return message.data[4] + ((message.data[5] & 0x7) << 8)
        def rrregenpowermax():
            return (message.data[7] * 4) - 200
        def rrdrivepowermax():
            return (((message.data[6] & 0x3F) << 5) + ((message.data[5] & 0xF0) >> 3)) + 1
        def rrdrivepowermaxhp():
            return rrdrivepowermax() * kw_to_hp
        def rrefficiency():
            return 1 if rrdissipation() < 1 else (rrmechpower() / rrmechpower() + rrdissipation() + 0.5) * 100

        if message.arbitration_id == 266:
            mqtt0 = publisher.publish(topic='RMotorEff', payload=rrefficiency())

        ##########################
        ###-648-288-rear-drive-ratio
        ##00 00 fc 7f 00
        ##########################

        def rearleft():
            return (message.data[4] + (message.data[3] << 8)) * 0.7371875 / 9.73
        def rearright():
            return (message.data[7] + (message.data[6] << 8)) * 0.7371875 / 9.73 # Does not work on my car
        def reardriveratio():
            return reardriveratio() if rrmotorrpm() > 1000 == 0 else (rearleft() + rearright()) /2 # Neither this one.

        ##########################
        ###-682-2AA-hvac
        ##2e 2e 52 41 01 00 00 00
        ##2e 2e 02 41 b1 00 00 00
        ##########################
        """def hvacfloor():
            return message.data[2] & 0x07
        if hvacfloor() == 1:
            print("HVAC Floor is pushing air to the seat.")
        if hvacfloor() == 2:
            print("HVAC is pushing air too feet and seats")
        if hvacfloor() == 3:
            print("HVAC is pushing air too feet")
        if hvacfloor() == 4:
            print("HVAC is pushing air too feet and windows")
        if hvacfloor() == 5:
            print("HVAC is pushing air too windows")
        if hvacfloor() == 6:
            print("HVAC is pushing air to feet, seat and windows")
        if hvacfloor() == 7:
            print("HVAC is pushing air to seat and windows")
"""
        def hvacrecycle():
            return (message.data[3] & 0x10) >> 4
        def hvacrecycletwo():
            return (message.data[3] & 0x8) >> 3
        def hvacac():
            return message.data[4] & 0x01
        def hvacstatus():
            return (message.data[3] & 0x10) >> 4
        def hvacfanspeed():
            return (message.data[2] & 0xf0) >> 4
        def hvactempleft():
            return message.data[0] / 2.0
        def hvactempright():
            return message.data[1] / 2.0




        ##########################
        ###-741-2E5-fr-multiple
        ##87 00 05 00 78 48 09 f6
        ##86 00 ff 07 14 48 09 f6
        ##########################
        #message.data = ([0x87, 0x00, 0x05, 0x00, 0x78, 0x48, 0x09, 0xf6])

        def frmechpower():
            return ((message.data[2] + ((message.data[3] & 0x7) << 8)) - (512 * (message.data[3] & 0x4))) / 2.0
        def frdissipation():
            return message.data[1] * 125.0 / 1000.0 - 0.5
        def frinputpower():
            return frmechpower() + frdissipation()
        def frmechpowerhp():
            return frmechpower() * kw_to_hp
        def frstatorcurrent():
            return message.data[4] + ((message.data[5] & 0x7) << 8)
        def frdrivepowermax():
            return (((message.data[6] & 0x3F) << 5) + ((message.data[5] & 0xF0) >> 3)) + 1
        def frdrivepowermaxhp():
            return frdrivepowermax() * kw_to_hp
        def mechpowercombined():
            return frmechpower() + rrmechpower()
        def hpcombined():
            return (frmechpower() + rrmechpower()) * kw_to_hp
        def frefficiency():
            return 1 if frdissipation() < 0 else (frmechpower() / frmechpower() + frdissipation() + 0.5) * 100
        def propulsion():
            return rrinputpower() + frinputpower()
        def totalhpmax():
            return frdrivepowermaxhp() + rrdrivepowermaxhp()
        if message.arbitration_id == 741:
            mqtt0 = publisher.publish(topic='FMotorEff', payload=frefficiency())
            mqtt1 = publisher.publish(topic='PropulsionkW', payload=propulsion())
            mqtt2 = publisher.publish(topic='HPUsageComb', payload=hpcombined())


        ##########################
        ###-770-302-ac-chargetotal
        ##54 27 0d 00 28 47 c7 00
        ##53 27 1d 00 8d 0a be 00
        ##########################

        def socmin():
            return (message.data[0] + ((message.data[1] & 0x3) << 8)) / 10.0
        def socui():
            return ((message.data[1] >> 2) + ((message.data[2] & 0xF) << 6)) / 10.0
        def dcchargetotal():
            return (message.data[4] + (message.data[5] << 8) + (message.data[6] << 16) + (message.data[7] << 24)) / 1000.0
        def acchargetotal():
            return (message.data[4] + (message.data[5] << 8) + (message.data[6] << 16) + (message.data[7] << 24)) / 1000.0
        """def charge():
            return message.data[2] >> 4
        if charge() == 0:
            print("DC Charge Total= ", dcchargetotal(), "kW")
        if charge() == 1:
            print("AC Charge Total= ", acchargetotal(), "kW")
"""

        ##########################
        ###-774-306-rear-coolant-inverter-etc
        ##37 33 35 34 33 00 4d 3f
        ##38 35 36 34 3a 00 4f 3f
        ##########################
        def coolant():
            return message.data[5]
        def rrcoolantinlettemp():
            return coolant() if coolant() == 0 else coolant() - 40
        def rrinverterpcbtemp():
            return message.data[0] - 40
        def rrstatortemp():
            return message.data[2] - 40
        def rrdccapacitortemp():
            return message.data[3] - 40
        def rrheatsinktemp():
            return message.data[4] - 40
        def rrinvertertemp():
            return message.data[1] - 40




        ##########################
        ###-776-308-louver
        ##e8 e9 0f 94 ae 46 00 00
        ##e8 e9 0f 94 ae 00 00 00
        ##########################
        def louver1():
            return (message.data[0] / 4) - 40
        def louver2():
            return (message.data[1] / 4) - 40
        def louver3():
            return (message.data[2] / 4) - 40
        def louver4():
            return (message.data[3] / 2) - 40
        def louver5():
            return (message.data[4] / 2) - 40
        def louver6():
            return (message.data[5] / 2) - 40
        def louver7():
            return (message.data[6] / 2) - 40
        def louver8():
            return (message.data[7] / 2) - 40

        ##########################
        ###-792-318-hvac-detailed
        ##59 59 77 14 62 ff ff 00
        ##5a 5a 75 14 62 ff ff 00
        ##########################

        def outsidetemp():
            return (message.data[0] / 2.0 - 40)
        def outsidetempfiltered():
            return (message.data[1] / 2.0 - 40)
        def insidetemp():
            return (message.data[2] / 2.0 - 40)
        def acairtemp():
            return (message.data[4] / 2.0 - 40)


        ##########################
        ###-794-31A-battery-inlet
        ##9b dd 25 a1 97 a9 0c 80
        ##9b dd 0a a1 9b a9 0b 80
        ##########################

        ##########################
        ###-898-382-battery
        ##aa f2 d1 8e 76 04 00 14
        ##aa ea d1 8e 76 04 00 14
        ##########################

        def nominalfullpack():
            return (message.data[0] + ((message.data[1] & 0x03) << 8)) * 0.1
        def nominalremaning():
            return ((message.data[1] >> 2) + ((message.data[2] & 0x0F) * 64)) * 0.1
        def expectedremaining():
            return ((message.data[2] >> 4) + ((message.data[3] & 0x3F) * 16)) * 0.1
        def idealremaining():
            return ((message.data[3] >> 6) + ((message.data[4] & 0xFF) * 4)) * 0.1
        def tochargecomplete():
            return (message.data[5] + ((message.data[6] & 0x03) << 8)) * 0.1
        def energybuffer():
            return ((message.data[6] >> 2) + ((message.data[7] & 0x03) * 64)) * 0.1
        def soc():
            return (nominalremaning() - energybuffer()) / (nominalfullpack() - energybuffer()) * 100
        def usablefullpack():
            return nominalfullpack() - energybuffer()
        def usableremaining():
            return nominalremaning() - energybuffer()






        ##########################
        ###-904-388-hvac-heater
        ##6e 69 4b 00 52 00 00 ff
        ##71 6b 50 00 5a 00 00 ff
        ##########################

        def floorl():
            return (message.data[1] / 2.0 - 20)
        def floorr():
            return (message.data[0] / 2.0 - 20)
        def othertemp1():
            return (message.data[2] / 2.0 - 20)
        def othertemp2():
            return (message.data[3] / 2.0 - 20)
        def othertemp3():
            return (message.data[4] / 2.0 - 20)
        def othertemp4():
            return (message.data[5] / 2.0 - 20)


        ##########################
        ###-978-3D2-discharge
        ##00 2d b9 01 b0 ff 9a 01
        ##06 2d b9 01 66 02 9b 01
        ##########################


        def chargetotal():
            return (message.data[0] + (message.data[1] << 8) + (message.data[2] << 16) + (message.data[3] << 24)) / 1000.0;
        def dischargetotal():
            return (message.data[4] + (message.data[5] << 8) + (message.data[6] << 16) + (message.data[7] << 24)) / 1000.0;
        def regenerated():
            return chargetotal() - acchargetotal() - dcchargetotal()
        def energy():
            return dischargetotal() - regenerated();
        def regen():
            return regenerated() / dischargetotal() * 100
        def dischargecycles():
            return dischargetotal() / nominalfullpack()
        def chargecycles():
            return chargetotal() / nominalfullpack()




        ##########################
        ###-1016-3F8-hvac-vents
        ##5e 03 bb 03 6c 03 a3 03
        ##3d 03 a9 03 51 03 88 03
        ##########################

        def floorventl():
            return ((message.data[4] + (message.data[5] << 8)) / 10.0) - 40
        def floorventr():
            return ((message.data[6] + (message.data[7] << 8)) / 10.0) - 40
        def midventl():
            return ((message.data[0] + (message.data[1] << 8)) / 10.0) - 40
        def midventr():
            return ((message.data[2] + (message.data[3] << 8)) / 10.0) - 40


        ##########################
        ###-1378-562-odometer
        ##b4 60 aa 03
        ##########################

        def batteryodometer():
            return (message.data[0] + (message.data[1] << 8) + (message.data[2] << 16) + (message.data[3] << 24)) / 1000.0 * miles_to_km


except KeyboardInterrupt:
    # Catch keyboard interrupt
    os.system("sudo /sbin/ip link set can0 down")

