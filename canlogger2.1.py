#!/usr/bin/python3
# Second iteration of Canlogger, patch1 moved around code for easier overview.

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
        ##########################
        ###-258-102-batteryvoltage
        ##########################
        def batteryvoltage():
            return (message.data[1] * 256 + message.data[0]) / 100.
        def batterycurrent():
            return (message.data[3] & 0x100000) * message.data[3] * 256 + message.data[2]
        def batterypower():
            return batterycurrent() * batteryvoltage() / 1000.0
        ##########################
        ###-262-106-rr-motor-rpm
        ##########################
        def rrmotorrpm():
            return (message.data[4] + (message.data[5] << 8)) - (512 * (message.data[5] & 0x80))
        ##########################
        ###-277-115-fr-motor-rpm
        ##########################
        def frmotorrpm():
            return (message.data[4] + (message.data[5] << 8)) - (512 * (message.data[5] & 0x80))
        ##########################
        ###-278-116-rr-torque-estimate
        ##########################
        def rrtorqueestimate():
            return ((message.data[0] + ((message.data[1] & 0xF) << 8)) - (512 * (message.data[1] & 0x8))) / 2
        def speed():
            return ((message.data[2] + ((message.data[3] & 0xF) << 8)) - 500) / 20.0 * miles_to_km
        def consumption():
            return batterypower() / speed() * 1000
        ##########################
        ###-325-145-fr-torque-estimate
        ##########################
        def frtorqueestimate():
            return ((message.data[0] + ((message.data[1] & 0xF) << 8)) - (512 * (message.data[1] & 0x8))) / 2
        ##########################
        ###-340-154-watt-pedal
        ##########################
        def rrtorquemeasured():
            return (message.data[5] + ((message.data[6] & 0x1F) << 8) - (512 * (message.data[6] & 0x10))) * 0.25
        def wattpedal():
            return message.data[3] * 0.4
        ##########################
        ###-468-1D4-fr-torque_torquebias
        ##########################
        def frtorquemeasured():
            return (message.data[5] + ((message.data[6] & 0x1F) << 8) - (512 * (message.data[6] & 0x10))) * 0.25
        def rrfrtorquebias():
            return 1 if frtorquemeasured() or rrtorquemeasured() < 1 else frtorquemeasured() / (rrtorquemeasured() + rrtorquemeasured()) * 100
        ##########################
        ###-528-210-dc-dc
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
        ##########################
        def maxbmsdischarge():
            return (message.data[2] + (message.data[3] << 8)) / 100.0
        def maxbmscharge():
            return (message.data[0] + (message.data[1] << 8)) / 100.0
        ##########################
        ###-614-266-rr-dissipation
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
        ##########################
        ###-648-288-rear-drive-ratio
        ##########################
        def rearleft():
            return (message.data[4] + (message.data[3] << 8)) * 0.7371875 / 9.73
        def rearright():
            return (message.data[7] + (message.data[6] << 8)) * 0.7371875 / 9.73 # Does not work on my car
        def reardriveratio():
            return reardriveratio() if rrmotorrpm() > 1000 == 0 else (rearleft() + rearright()) /2 # Neither this one.
        ##########################
        ###-682-2AA-hvac
        ##########################
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
        def hvacfloor():
            return message.data[2] & 0x07
        def hvacfloorstatus():
            if hvacfloor() == 1:
                return "Seat"
            if hvacfloor() == 2:
                return "Feet and Seat"
            if hvacfloor() == 3:
                return "Feet"
            if hvacfloor() == 4:
                return "Feet and Windows"
            if hvacfloor() == 5:
                return "Windows"
            if hvacfloor() == 6:
                return "Feet, Seat and Windows"
            if hvacfloor() == 7:
                return "Seat and Windows"
        ##########################
        ###-741-2E5-fr-multiple
        ##########################
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
        ##########################
        ###-770-302-ac-chargetotal
        ##########################
        def socmin():
            return (message.data[0] + ((message.data[1] & 0x3) << 8)) / 10.0
        def socui():
            return ((message.data[1] >> 2) + ((message.data[2] & 0xF) << 6)) / 10.0
        def chargecalc():
            return message.data[2] >> 4
        def dcchargetotal():
            return (message.data[4] + (message.data[5] << 8) + (message.data[6] << 16) + (message.data[7] << 24)) / 1000.0 if chargecalc() == 0 else 0
        def acchargetotal():
            return (message.data[4] + (message.data[5] << 8) + (message.data[6] << 16) + (message.data[7] << 24)) / 1000.0 if chargecalc() == 1 else 0
        ##########################
        ###-774-306-rear-coolant-inverter-etc
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
        ##########################
        # FUTURE FUNCTION.
        ##########################
        ###-898-382-battery
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
        ##########################
        def batteryodometer():
            return (message.data[0] + (message.data[1] << 8) + (message.data[2] << 16) + (message.data[3] << 24)) / 1000.0 * miles_to_km


        if message.arbitration_id == 14:
            mqtt0 = publisher.publish(topic='steeringangle', payload=steeringangle())
        if message.arbitration_id == 256:
            mqtt0 = publisher.publish(topic='batteryvoltage', payload=batteryvoltage())
            mqtt1 = publisher.publish(topic='batterycurrent', payload=batterycurrent())
            mqtt2 = publisher.publish(topic='batterypower', payload=batterypower())
        if message.arbitration_id == 262:
            mqtt0 = publisher.publish(topic='rmotorrpm', payload=rrmotorrpm())
        if message.arbitration_id == 277:
            mqtt0 = publisher.publish(topic='fmotorrpm', payload=frmotorrpm())
        if message.arbitration_id == 278:
            mqtt0 = publisher.publish(topic='rrtorqueestimate', payload=rrtorqueestimate())
            mqtt1 = publisher.publish(topic='speed', payload=speed())
            mqtt2 = publisher.publish(topic='consumption', payload=consumption())
        if message.arbitration_id == 325:
            mqtt0 = publisher.publish(topic='frtorqueestimate', payload=frtorqueestimate())
        if message.arbitration_id == 340:
            mqtt0 = publisher.publish(topic='rrtorquemeasured', payload=rrtorquemeasured())
            mqtt1 = publisher.publish(topic='wattpedal', payload=wattpedal())
        if message.arbitration_id == 468:
            mqtt0 = publisher.publish(topic='frtorquemeasured', payload=frtorquemeasured())
            mqtt1 = publisher.publish(topic='rrfrtorquebias', payload=rrfrtorquebias())
        if message.arbitration_id == 528:
            mqtt0 = publisher.publish(topic='dcdccurrent', payload=dcdccurrent())
            mqtt1 = publisher.publish(topic='dcdcvoltage', payload=dcdcvoltage())
            mqtt2 = publisher.publish(topic='dcdccoolantinlet', payload=dcdccoolantinlet())
            mqtt3 = publisher.publish(topic='dcdcinputpower', payload=dcdcinputpower())
            mqtt4 = publisher.publish(topic='twelvevoltsystem', payload=twelvevoltsystem())
            mqtt5 = publisher.publish(topic='dcdcoutputpower', payload=dcdcoutputpower())
            mqtt6 = publisher.publish(topic='dcdcefficiency', payload=dcdcefficiency())
            mqtt7 = publisher.publish(topic='fourhundredvoltsystem', payload=fourhundredvoltsystem())
        if message.arbitration_id == 562:
            mqtt0 = publisher.publish(topic='maxbmsdischarge', payload=maxbmsdischarge())
            mqtt1 = publisher.publish(topic='maxbmscharge', payload=maxbmscharge())
        if message.arbitration_id == 614:
            mqtt0 = publisher.publish(topic='rrinverterwvelvevolt', payload=rrinvertertwelvevolt())
            mqtt1 = publisher.publish(topic='rrmechpower', payload=rrmechpower())
            mqtt2 = publisher.publish(topic='rrdissipation', payload=rrdissipation())
            mqtt3 = publisher.publish(topic='rrinputpower', payload=rrinputpower())
            mqtt4 = publisher.publish(topic='rrmechpowerhp', payload=rrmechpowerhp())
            mqtt5 = publisher.publish(topic='rrstatorcurrent', payload=rrstatorcurrent())
            mqtt6 = publisher.publish(topic='rrregenpowermax', payload=rrregenpowermax())
            mqtt7 = publisher.publish(topic='rrdrivepowermax', payload=rrdrivepowermax())
            mqtt8 = publisher.publish(topic='rrdrivepowermaxhp', payload=rrdrivepowermaxhp())
            mqtt9 = publisher.publish(topic='rrefficiency', payload=rrefficiency())
        if message.arbitration_id == 648:
            mqtt0 = publisher.publish(topic='rearleft', payload=rearleft())
            mqtt1 = publisher.publish(topic='rearright', payload=rearright())
            mqtt2 = publisher.publish(topic='reardriveratio', payload=reardriveratio())
        if message.arbitration_id == 628:
            mqtt0 = publisher.publish(topic='hvacrecycle', payload=hvacrecycle())
            mqtt1 = publisher.publish(topic='hvacrecycletwo', payload=hvacrecycletwo())
            mqtt2 = publisher.publish(topic='hvacac', payload=hvacac())
            mqtt3 = publisher.publish(topic='hvacstatus', payload=hvacstatus())
            mqtt4 = publisher.publish(topic='hvacfanspeed', payload=hvacfanspeed())
            mqtt5 = publisher.publish(topic='hvactempleft', payload=hvactempleft())
            mqtt6 = publisher.publish(topic='hvactempright', payload=hvactempright())
            mqtt7 = publisher.publish(topic='hvacfloorstatur', payload=hvacfloorstatus())
        if message.arbitration_id == 741:
            mqtt0 = publisher.publish(topic='frmechpower', payload=frmechpower())
            mqtt1 = publisher.publish(topic='frdissipation', payload=frdissipation())
            mqtt2 = publisher.publish(topic='frinputpower', payload=frinputpower())
            mqtt3 = publisher.publish(topic='frmechpowerhp', payload=frmechpowerhp())
            mqtt4 = publisher.publish(topic='frstatorcurrent', payload=frstatorcurrent())
            mqtt5 = publisher.publish(topic='frdrivepowermax', payload=frdrivepowermax())
            mqtt6 = publisher.publish(topic='frdrivepowermaxhp', payload=frdrivepowermaxhp())
            mqtt7 = publisher.publish(topic='mechpowercombined', payload=mechpowercombined())
            mqtt8 = publisher.publish(topic='hpcombined', payload=hpcombined())
            mqtt9 = publisher.publish(topic='frefficiency', payload=frefficiency())
            mqtt10 = publisher.publish(topic='propulsion', payload=propulsion())
            mqtt11 = publisher.publish(topic='totalhpmax', payload=totalhpmax())
        if message.arbitration_id == 770:
            mqtt0 = publisher.publish(topic='socmin', payload=socmin())
            mqtt1 = publisher.publish(topic='socui', payload=socui())
            mqtt2 = publisher.publish(topic='dcchargetotal', payload=dcchargetotal())
            mqtt3 = publisher.publish(topic='acchargetotal', payload=acchargetotal())
        if message.arbitration_id == 774:
            mqtt0 = publisher.publish(topic='coolant', payload=coolant())
            mqtt1 = publisher.publish(topic='rrcoolantinlettemp', payload=rrcoolantinlettemp())
            mqtt2 = publisher.publish(topic='rrinverterpcbtemp', payload=rrinverterpcbtemp())
            mqtt3 = publisher.publish(topic='rrstatortemp', payload=rrstatortemp())
            mqtt4 = publisher.publish(topic='rrdccapacitortemp', payload=rrdccapacitortemp())
            mqtt5 = publisher.publish(topic='rrheatsinktemp', payload=rrheatsinktemp())
            mqtt6 = publisher.publish(topic='rrinvertertemp', payload=rrinvertertemp())
        if message.arbitration_id == 776:
            mqtt0 = publisher.publish(topic='louver1', payload=louver1())
            mqtt1 = publisher.publish(topic='louver2', payload=louver2())
            mqtt2 = publisher.publish(topic='louver3', payload=louver3())
            mqtt3 = publisher.publish(topic='louver4', payload=louver4())
            mqtt4 = publisher.publish(topic='louver5', payload=louver5())
            mqtt5 = publisher.publish(topic='louver6', payload=louver6())
            mqtt6 = publisher.publish(topic='louver7', payload=louver7())
            mqtt7 = publisher.publish(topic='louver8', payload=louver8())
        if message.arbitration_id == 792:
            mqtt0 = publisher.publish(topic='outsidetemp', payload=outsidetemp())
            mqtt1 = publisher.publish(topic='outsidetempfiltered', payload=outsidetempfiltered())
            mqtt2 = publisher.publish(topic='insidetemp', payload=insidetemp())
            mqtt3 = publisher.publish(topic='acairtemp', payload=acairtemp())
        if message.arbitration_id == 898:
            mqtt0 = publisher.publish(topic='nominalfullpack', payload=nominalfullpack())
            mqtt1 = publisher.publish(topic='nominalremaining', payload=nominalremaning())
            mqtt2 = publisher.publish(topic='expectedremaining', payload=expectedremaining())
            mqtt3 = publisher.publish(topic='idealremaining', payload=idealremaining())
            mqtt4 = publisher.publish(topic='tochargecomplete', payload=tochargecomplete())
            mqtt5 = publisher.publish(topic='energybuffer', payload=energybuffer())
            mqtt6 = publisher.publish(topic='soc', payload=soc())
            mqtt7 = publisher.publish(topic='usablefullpack', payload=usablefullpack())
            mqtt8 = publisher.publish(topic='usableremaining', payload=usableremaining())
        if message.arbitration_id == 904:
            mqtt0 = publisher.publish(topic='floorl', payload=floorl())
            mqtt1 = publisher.publish(topic='floorr', payload=floorr())
            mqtt2 = publisher.publish(topic='othertemp1', payload=othertemp1())
            mqtt3 = publisher.publish(topic='othertemp2', payload=othertemp2())
            mqtt4 = publisher.publish(topic='othertemp3', payload=othertemp3())
            mqtt5 = publisher.publish(topic='othertemp4', payload=othertemp4())
        if message.arbitration_id == 978:
            mqtt0 = publisher.publish(topic='chargetotal', payload=chargetotal())
            mqtt1 = publisher.publish(topic='dischargetotal', payload=dischargetotal())
            mqtt2 = publisher.publish(topic='regenerated', payload=regenerated())
            mqtt3 = publisher.publish(topic='energy', payload=energy())
            mqtt4 = publisher.publish(topic='regen', payload=regen())
            mqtt5 = publisher.publish(topic='dischargecycles', payload=dischargecycles())
            mqtt6 = publisher.publish(topic='chargecycles', payload=chargecycles())
        if message.arbitration_id == 1016:
            mqtt0 = publisher.publish(topic='floorventl', payload=floorventl())
            mqtt1 = publisher.publish(topic='floorventr', payload=floorventr)
            mqtt2 = publisher.publish(topic='midventl', payload=midventl)
            mqtt3 = publisher.publish(topic='midventr', payload=midventr)
        if message.arbitration_id == 1378:
            mqtt0 = publisher.publish(topic='batteryodometer', payload=batteryodometer())


except KeyboardInterrupt:
    # Catch keyboard interrupt
    os.system("sudo /sbin/ip link set can0 down")

