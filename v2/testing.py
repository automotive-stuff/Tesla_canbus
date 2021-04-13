#!/usr/bin/python3
# First script, logging to a file.

#Main import.

import sys
import glob
import time, datetime
import io
import os
import can
import csv


#Some settings to make life easier.

#VARIABLES

miles_to_km = 1.609344
kw_to_hp = 1.34102209


##########################
###-14-00E-steeringangle
##20 40 20 00 04 ff 60 27
##14 93 20 2f 04 ff 90 eb
##########################
fjorton = ([0x00, 0x40, 0x20, 0x00, 0x04, 0xff, 0xc0, 0x86])

def steeringangle():
    return (((fjorton[0] << 8) + fjorton[1] - 8200.0) / 10.0)
print("###-14-00E-steeringangle")
print("SteeringAngle= ", steeringangle(), "Degrees")
print("##########################")
##########################
###-258-102-batteryvoltage
##09 85 ba ff c0 ff fc 1f
##fb 84 bd ff ad ff fc 1f
##########################
ettnolltva = ([0x09, 0x85, 0xba, 0xff, 0xc0, 0xff, 0xfc, 0x1f])

def batteryvoltage():
    return (ettnolltva[1] * 256 + ettnolltva[0]) / 100.
def batterycurrent():
    return (ettnolltva[3] & 0x100000) * ettnolltva[3] * 256 + ettnolltva[2]
def batterypower():
    return batterycurrent() * batteryvoltage() / 1000.0
print("###-258-102-batteryvoltage")
print("BatteryVoltage= ", batteryvoltage(), "V")
print("BatteryAmps= ", batterycurrent(), "A")
print("BatteryPower= ", batterypower(), "kW")
print("##########################")
##########################
###-262-106-rr-motor-rpm
##00 20 00 80 00 00 00 a7
##90 60 8c 80 13 00 20 36
##########################
tvasextva = ([0x90, 0x60, 0x8c, 0x80, 0x13, 0x00, 0x20, 0x36])

def rrmotorrpm():
    return (tvasextva[4] + (tvasextva[5] << 8)) - (512 * (tvasextva[5] & 0x80))
print("###-262-106-rr-motor-rpm")
print("Rear Motor= ", rrmotorrpm(), "RPM")
print("##########################")
##########################
###-277-115-fr-motor-rpm
##00 e0 00 80 00 00 76
##99 a0 96 80 23 00 88
##########################
tvasjusju = ([0x99, 0xa0, 0x96, 0x80, 0x23, 0x00, 0x88])

def frmotorrpm():
    return (tvasjusju[4] + (tvasjusju[5] << 8)) - (512 * (tvasjusju[5] & 0x80))
print("###-277-115-fr-motor-rpm")
print("Front Motor= ", frmotorrpm(), "RPM")
print("##########################")
##########################
###-278-116-rr-torque-estimate
##ff 1f f4 11 8b c5
##65 40 00 42 8b 89
##########################
tvasjuatta = ([0x65, 0x40, 0x00, 0x42, 0x8b, 0x89])

def rrtorqueestimate():
    return ((tvasjuatta[0] + ((tvasjuatta[1] & 0xF) << 8)) - (512 * (tvasjuatta[1] & 0x8))) / 2
def speed():
    return ((tvasjuatta[2] + ((tvasjuatta[3] & 0xF) << 8)) - 500) / 20.0 * miles_to_km
def consumption():
    return batterypower() / speed() * 1000
print("###-278-116-rr-torque-estimate")
print("RearMotor Torque Estimate= ", rrtorqueestimate(), "Nm")
print("Speed= ", speed(), "km/h")
print("Consumption= ", consumption(), "wh|km")
print("##########################")
##########################
###-325-145-fr-torque-estimate
##ff cf 14
##60 e0 86
##########################
tretvafem = ([0xff, 0xcf, 0x14])

def frtorqueestimate():
    return ((tretvafem[0] + ((tretvafem[1] & 0xF) << 8)) - (512 * (tretvafem[1] & 0x8))) / 2
print("###-325-145-fr-torque-estimate")
print("FrontMotor Torque Estimate= ", frtorqueestimate(), "Nm")
print("##########################")
##########################
###-340-154-watt-pedal
##18 32 10 00 00 ff 3f ed
##18 b2 10 20 1d 92 40 3e
##########################
trefyranoll = ([0x18, 0xb2, 0x10, 0x20, 0x1d, 0x92, 0x40, 0x3e])

def rrtorquemeasured():
    return (trefyranoll[5] + ((trefyranoll[6] & 0x1F) << 8) - (512 * (trefyranoll[6] & 0x10))) * 0.25
def wattpedal():
    return trefyranoll[3] * 0.4
print("###-340-154-watt-pedal")
print("Rear Motor Torque Measured= ", rrtorquemeasured(), "Nm")
print("WattPedal= ", wattpedal(), "%")
print("##########################")
##########################
###-468-1D4-fr-torque_torquebias
##00 04 00 00 08 7f 60 c0
##00 04 00 00 08 b4 3f d4
##########################
fyrasexatta = ([0x00, 0x04, 0x00, 0x00, 0x08, 0x7f, 0x60, 0xc0])
def frtorquemeasured():
    return (fyrasexatta[5] + ((fyrasexatta[6] & 0x1F) << 8) - (512 * (fyrasexatta[6] & 0x10))) * 0.25
def rrfrtorquebias():
    return rrfrtorquebias() if frtorquemeasured() > rrtorquemeasured() == 0 else frtorquemeasured() / (rrtorquemeasured() + rrtorquemeasured()) * 100
print("###-468-1D4-fr-torque_torquebias")
print("Front Torque Measured= ", frtorquemeasured(), "Nm")
print("Front / Rear Torque Bias= ", rrfrtorquebias(), "%")
print("##########################")
##########################
###-528-210-dc-dc
##00 00 cc 17 18 89 00
##00 00 ca 1b 1e 89 00
##########################
femtvaatta =([0x00, 0x00, 0xca, 0x1b, 0x1e, 0x89, 0x00])
def dcdccurrent():
    return femtvaatta[4]
def dcdcvoltage():
    return femtvaatta[5] / 10.0
def dcdccoolantinlet():
    return ((femtvaatta[2] - (2 * (femtvaatta[2] & 0x80))) * 0.5) + 40
def dcdcinputpower():
    return (femtvaatta[3] * 16)
def twelvevoltsystem():
    return (femtvaatta[3] * 16)
def dcdcoutputpower():
    return (femtvaatta[4] * femtvaatta[5] / 10.0)
def dcdcefficiency():
    return dcdcoutputpower() / dcdcinputpower() * 100.0
def fourhundredvoltsystem():
    return batterypower() - dcdcinputpower() / 1000.0
print("###-528-210-dc-dc")
print("HVDC-12VDC Current= ", dcdccurrent(), "A")
print("HVDC-12VDC Voltage= ", dcdcvoltage(), "V")
print("DC-DC Coolant Inlet= ", dcdccoolantinlet(), "C")
print("HVDC-12VDC Power Draw= ", dcdcinputpower(), "W")
print("12V Systems Consumption= ", twelvevoltsystem(), "W")
print("DC-DC Provided Power= ", dcdcoutputpower(), "W")
print("DC-DC Efficiency= ", dcdcefficiency(), "%")
print("400V Systems= ", fourhundredvoltsystem(), "kW")
print("##########################")
##########################
###-562-232-max-discharge
##51 08 f0 7e
##4c 08 e6 7e
##########################
femsextva = ([0x51, 0x08, 0xf0, 0x7e])
def maxbmsdischarge():
    return (femsextva[2] + (femsextva[3] << 8)) / 100.0
def maxbmscharge():
    return (femsextva[0] + (femsextva[1] << 8)) / 100.0
print("###-562-232-max-discharge")
print("Max BMS Discharge= ", maxbmsdischarge(), "kW")
print("Max BMS Charge= ", maxbmscharge(), "kW")
print("##########################")
##########################
###-614-266-rr-dissipation
##87 02 00 00 00 28 4a 38
##87 02 09 00 80 28 0a 38
##########################
sexettfyra = ([0x87, 0x02, 0x09, 0x00, 0x80, 0x28, 0x0a, 0x38])
def rrinvertertwelvevolt():
    return sexettfyra[0] / 10.0
def rrmechpower():
    return ((sexettfyra[2] + ((sexettfyra[3] & 0x7) << 8)) - (512 * (sexettfyra[3] & 0x4))) / 2.0
def rrdissipation():
    return sexettfyra[1] * 125.0 / 1000.0 - 0.5
def rrinputpower():
    return rrmechpower() + rrdissipation()
def rrmechpowerhp():
    return rrmechpower() * kw_to_hp
def rrstatorcurrent():
    return sexettfyra[4] + ((sexettfyra[5] & 0x7) << 8)
def rrregenpowermax():
    return (sexettfyra[7] * 4) - 200
def rrdrivepowermax():
    return (((sexettfyra[6] & 0x3F) << 5) + ((sexettfyra[5] & 0xF0) >> 3)) + 1
def rrdrivepowermaxhp():
    return rrdrivepowermax() * kw_to_hp
def rrefficiency():
    return rrefficiency() if rrdissipation() > 0.0 == 0 else (rrmechpower() / rrmechpower() + rrdissipation() + 0.5) * 100

print("###-614-266-rr-dissipation")
print("Rear Inverter 12V= ", rrinvertertwelvevolt(), "V")
print("Rear Mech Power= ", rrmechpower(), "kW")
print("Rear Dissipation= ", rrdissipation(), "kW")
print("Rear Input Power= ", rrinputpower(), "kW")
print("Rear Mech Power Usage= ", rrmechpowerhp(), "HP")
print("Rear Stator Current= ", rrstatorcurrent(), "A")
print("Rear RegenPower Max= ", rrregenpowermax(), "kW")
print("Rear DrivePower Max= ", rrdrivepowermaxhp(), "HP")
print("Rear DrivePower Max= ", rrdrivepowermax(), "kW")
print("Rear Efficiency= ", rrefficiency(), "%")
print("##########################")
##########################
###-648-288-rear-drive-ratio
##00 00 fc 7f 00
##########################
sexfyraatta = ([0x00, 0x00, 0xfc, 0x7f, 0x00])

def rearleft():
    return (sexfyraatta[4] + (sexfyraatta[3] << 8)) * 0.7371875 / 9.73
def rearright():
    return (sexfyraatta[7] + (sexfyraatta[6] << 8)) * 0.7371875 / 9.73 # Does not work on my car
def reardriveratio():
    return reardriveratio() if rrmotorrpm() > 1000 == 0 else (rearleft() + rearright()) /2 # Neither this one.
print("###-648-288-rear-drive-ratio")
print("Rear Left motor= ", rearleft(), "RPM")
#print("Rear Right motor= ", rearright(), "RPM")
#print("Rear Drive Ratio= ", reardriveratio())
print("##########################")
##########################
###-682-2AA-hvac
##2e 2e 52 41 01 00 00 00
##2e 2e 02 41 b1 00 00 00
##########################
print("###-682-2AA-hvac")
sexattatva =  ([0x2e, 0x2e, 0x52, 0x41, 0x01, 0x00, 0x00, 0x00])
def hvacfloor():
    return sexattatva[2] & 0x07
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

def hvacrecycle():
    return (sexattatva[3] & 0x10) >> 4
def hvacrecycletwo():
    return (sexattatva[3] & 0x8) >> 3
def hvacac():
    return sexattatva[4] & 0x01
def hvacstatus():
    return (sexattatva[3] & 0x10) >> 4
def hvacfanspeed():
    return (sexattatva[2] & 0xf0) >> 4
def hvactempleft():
    return sexattatva[0] / 2.0
def hvactempright():
    return sexattatva[1] / 2.0

print("HVAC Recycle= ", hvacrecycle())
print("HVAC Recycle2= ", hvacrecycletwo())
print("HVAC AC= ", hvacac())
print("HVAC Status= ", hvacstatus())
print("HVAC Fanspeed= ", hvacfanspeed())
print("HVAC Left Temperature= ", hvactempleft())
print("HVAC Right Temperature= ", hvactempright())
print("##########################")


##########################
###-741-2E5-fr-multiple
##87 00 05 00 78 48 09 f6
##86 00 ff 07 14 48 09 f6
##########################
sjufyraett = ([0x87, 0x00, 0x05, 0x00, 0x78, 0x48, 0x09, 0xf6])

def frmechpower():
    return ((sjufyraett[2] + ((sjufyraett[3] & 0x7) << 8)) - (512 * (sjufyraett[3] & 0x4))) / 2.0
def frdissipation():
    return sjufyraett[1] * 125.0 / 1000.0 - 0.5
def frinputpower():
    return frmechpower() + frdissipation()
def frmechpowerhp():
    return frmechpower() * kw_to_hp
def frstatorcurrent():
    return sjufyraett[4] + ((sjufyraett[5] & 0x7) << 8)
def frdrivepowermax():
    return (((sjufyraett[6] & 0x3F) << 5) + ((sjufyraett[5] & 0xF0) >> 3)) + 1
def frdrivepowermaxhp():
    return frdrivepowermax() * kw_to_hp
def mechpowercombined():
    return frmechpower() + rrmechpower()
def hpcombined():
    return (frmechpower() + rrmechpower()) * kw_to_hp
def frefficiency():
    return frefficiency() if frdissipation() > 0.0 == 0 else (frmechpower() / frmechpower() + frdissipation() + 0.5) * 100
def propulsion():
    return rrinputpower() + frinputpower()
def totalhpmax():
    return frdrivepowermaxhp() + rrdrivepowermaxhp()

print("###-741-2E5-fr-multiple")
print("Front Mech power= ", frmechpower(), "kW")
print("Front Dissipation= ", frdissipation(), "kW")
print("Front Input Power= ", frinputpower(), "kW")
print("Front Mech Power= ", frmechpowerhp(), "HP")
print("Front Stator Current= ", frstatorcurrent(), "A")
print("Front DrivePower Max= ", frdrivepowermax(), "kW")
print("Front DrivePower Max= ", frdrivepowermaxhp(), "HP")
print("Mech Power Usage Combined= ", mechpowercombined(), "kW")
print("HP Usage Combined= ", hpcombined(), "HP")
print("Front Efficiency= ", frefficiency(), "%")
print("Propulsion= ", propulsion(), "kW")
print("Combined Power Max= ", totalhpmax(), "HP")

print("##########################")
##########################
###-770-302-ac-chargetotal
##54 27 0d 00 28 47 c7 00
##53 27 1d 00 8d 0a be 00
##########################
print("###-770-302-ac-chargetotal")
sjusjutio = ([0x54, 0x27, 0x0d, 0x00, 0x28, 0x47, 0xc7, 0x00])
def socmin():
    return (sjusjutio[0] + ((sjusjutio[1] & 0x3) << 8)) / 10.0
def socui():
    return ((sjusjutio[1] >> 2) + ((sjusjutio[2] & 0xF) << 6)) / 10.0
def dcchargetotal():
    return (sjusjutio[4] + (sjusjutio[5] << 8) + (sjusjutio[6] << 16) + (sjusjutio[7] << 24)) / 1000.0
def acchargetotal():
    return (sjusjutio[4] + (sjusjutio[5] << 8) + (sjusjutio[6] << 16) + (sjusjutio[7] << 24)) / 1000.0
def charge():
    return sjusjutio[2] >> 4
if charge() == 0:
    print("DC Charge Total= ", dcchargetotal(), "kW")
if charge() == 1:
    print("AC Charge Total= ", acchargetotal(), "kW")

print("Soc Min= ", socmin(), "%")
print("Soc UI= ", socui(), "%")
print("##########################")
##########################
###-774-306-rear-coolant-inverter-etc
##37 33 35 34 33 00 4d 3f
##38 35 36 34 3a 00 4f 3f
##########################
sjusjutiofyra = ([0x37, 0x33, 0x35, 0x34, 0x33, 0x00, 0x4d, 0x3f])
def coolant():
    return sjusjutiofyra[5]
def rrcoolantinlettemp():
    return coolant() if coolant() == 0 else coolant() - 40
def rrinverterpcbtemp():
    return sjusjutiofyra[0] - 40
def rrstatortemp():
    return sjusjutiofyra[2] - 40
def rrdccapacitortemp():
    return sjusjutiofyra[3] - 40
def rrheatsinktemp():
    return sjusjutiofyra[4] - 40
def rrinvertertemp():
    return sjusjutiofyra[1] - 40

print("###-774-306-rear-coolant-inverter-etc")
print("Rear Coolant inlet= ", rrcoolantinlettemp(), "C")
print("Rear Inverter PCB= ", rrinverterpcbtemp(), "C")
print("Rear Stator= ", rrstatortemp(), "C")
print("Rear DC Capacitor= ", rrdccapacitortemp(), "C")
print("Rear Heatsink= ", rrheatsinktemp(), "C")
print("Rear Inverter= ", rrinvertertemp(), "C")
print("##########################")


##########################
###-776-308-louver
##e8 e9 0f 94 ae 46 00 00
##e8 e9 0f 94 ae 00 00 00
##########################
sjusjutiosex = ([0xe8, 0xe9, 0x0f, 0x94, 0xae, 0x46, 0x00, 0x00])
def louver1():
    return (sjusjutiosex[0] / 4) - 40
def louver2():
    return (sjusjutiosex[1] / 4) - 40
def louver3():
    return (sjusjutiosex[2] / 4) - 40
def louver4():
    return (sjusjutiosex[3] / 2) - 40
def louver5():
    return (sjusjutiosex[4] / 2) - 40
def louver6():
    return (sjusjutiosex[5] / 2) - 40
def louver7():
    return (sjusjutiosex[6] / 2) - 40
def louver8():
    return (sjusjutiosex[7] / 2) - 40
print("###-776-308-louver")
print("Louver 1= ", louver1(), "C")
print("Louver 2= ", louver2(), "C")
print("Louver 3= ", louver3(), "C")
print("Louver 4= ", louver4(), "C")
print("Louver 5= ", louver5(), "C")
print("Louver 6= ", louver6(), "C")
print("Louver 7= ", louver7(), "C")
print("Louver 8= ", louver8(), "C")
print("##########################")
##########################
###-792-318-hvac-detailed
##59 59 77 14 62 ff ff 00
##5a 5a 75 14 62 ff ff 00
##########################
sjunittiotva = ([0x59, 0x59, 0x77, 0x14, 0x62, 0xff, 0xff, 0x00])

def outsidetemp():
    return (sjunittiotva[0] / 2.0 - 40)
def outsidetempfiltered():
    return (sjunittiotva[1] / 2.0 - 40)
def insidetemp():
    return (sjunittiotva[2] / 2.0 - 40)
def acairtemp():
    return (sjunittiotva[4] / 2.0 - 40)

print("###-792-318-hvac-detailed")
print("Outside Temp= ", outsidetemp(), "C")
print("Outside Temp Filtered= ", outsidetempfiltered(), "C")
print("Inside Temp= ", insidetemp(), "C")
print("A/C Air Temp= ", acairtemp(), "C")
print("##########################")
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
attanittioatta = ([0xaa, 0xf2, 0xd1, 0x8e, 0x76, 0x04, 0x00, 0x14])

def nominalfullpack():
    return (attanittioatta[0] + ((attanittioatta[1] & 0x03) << 8)) * 0.1
def nominalremaning():
    return ((attanittioatta[1] >> 2) + ((attanittioatta[2] & 0x0F) * 64)) * 0.1
def expectedremaining():
    return ((attanittioatta[2] >> 4) + ((attanittioatta[3] & 0x3F) * 16)) * 0.1
def idealremaining():
    return ((attanittioatta[3] >> 6) + ((attanittioatta[4] & 0xFF) * 4)) * 0.1
def tochargecomplete():
    return (attanittioatta[5] + ((attanittioatta[6] & 0x03) << 8)) * 0.1
def energybuffer():
    return ((attanittioatta[6] >> 2) + ((attanittioatta[7] & 0x03) * 64)) * 0.1
def soc():
    return (nominalremaning() - energybuffer()) / (nominalfullpack() - energybuffer()) * 100
def usablefullpack():
    return nominalfullpack() - energybuffer()
def usableremaining():
    return nominalremaning() - energybuffer()


print("###-898-382-battery")
print("Nominal Full Pack= ", nominalfullpack(), "kW")
print("Nominal Remaining= ", nominalremaning(), "kW")
print("Expected Remaining= ", expectedremaining(), "kW")
print("Ideal Remaining= ", idealremaining(), "kW")
print("To Charge Complete= ", tochargecomplete(), "kW")
print("EnergyBuffer= ", energybuffer(), "kW")
print("SOC = ", soc(), "%")
print("Usable Full Pack= ", usablefullpack(), "kW")
print("Usable Remaining= ", usableremaining(), "kW")
print("##########################")



##########################
###-904-388-hvac-heater
##6e 69 4b 00 52 00 00 ff
##71 6b 50 00 5a 00 00 ff
##########################
nittionollfyra = ([0x6e, 0x69, 0x4b, 0x00, 0x52, 0x00, 0x00, 0xff])

def floorl():
    return (nittionollfyra[1] / 2.0 - 20)
def floorr():
    return (nittionollfyra[0] / 2.0 - 20)
def othertemp1():
    return (nittionollfyra[2] / 2.0 - 20)
def othertemp2():
    return (nittionollfyra[3] / 2.0 - 20)
def othertemp3():
    return (nittionollfyra[4] / 2.0 - 20)
def othertemp4():
    return (nittionollfyra[5] / 2.0 - 20)

print("###-904-388-hvac-heater")
print("Floor L= ", floorl(), "C")
print("Floor R= ", floorr(), "C")
print("other 1= ", othertemp1(), "C")
print("other 2= ", othertemp2(), "C")
print("other 3= ", othertemp3(), "C")
print("other 4= ", othertemp4(), "C")
print("##########################")

##########################
###-978-3D2-discharge
##00 2d b9 01 b0 ff 9a 01
##06 2d b9 01 66 02 9b 01
##########################

print("###-978-3D2-discharge")
niosjuatta = ([0x00, 0x2d, 0xb9, 0x01, 0xb0, 0xff, 0x9a, 0x01])

def chargetotal():
    return (niosjuatta[0] + (niosjuatta[1] << 8) + (niosjuatta[2] << 16) + (niosjuatta[3] << 24)) / 1000.0;
def dischargetotal():
    return (niosjuatta[4] + (niosjuatta[5] << 8) + (niosjuatta[6] << 16) + (niosjuatta[7] << 24)) / 1000.0;
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


print("Charge Total= ", chargetotal(), "kWh")
print("Discharge Total= ", dischargetotal(), "kWh")
print("total Regen= ", regenerated(), "kWh")
print("Energy = ", energy(), "kWh")
print("Regen= ", regen(), "%")
print("regen=", format(regen(), ".2f"))
print("Discharge Cycles= ", dischargecycles())
print("Charge Cycles= ", chargecycles())

print("##########################")



##########################
###-1016-3F8-hvac-vents
##5e 03 bb 03 6c 03 a3 03
##3d 03 a9 03 51 03 88 03
##########################
ettnollettsex = ([0x5e, 0x03, 0xbb, 0x03, 0x6c, 0x03, 0xa3, 0x03])

def floorventl():
    return ((ettnollettsex[4] + (ettnollettsex[5] << 8)) / 10.0) - 40
def floorventr():
    return ((ettnollettsex[6] + (ettnollettsex[7] << 8)) / 10.0) - 40
def midventl():
    return ((ettnollettsex[0] + (ettnollettsex[1] << 8)) / 10.0) - 40
def midventr():
    return ((ettnollettsex[2] + (ettnollettsex[3] << 8)) / 10.0) - 40

print("###-1016-3F8-hvac-vents")
print("Floor Vent L= ", floorventl(), "C")
print("Floor Vent R= ", floorventr(), "C")
print("Mid Vent L= ", midventl(), "C")
print("Mid Vent R= ", midventr(), "C")
print("##########################")
##########################
###-1378-562-odometer
##b4 60 aa 03
##########################
etttresjuatta = ([0xb4, 0x60, 0xaa, 0x03])
print("###-1378-562-odometer")

def batteryodometer():
    return (etttresjuatta[0] + (etttresjuatta[1] << 8) + (etttresjuatta[2] << 16) + (etttresjuatta[3] << 24)) / 1000.0 * miles_to_km

print("Odometer = ", batteryodometer(), "km")
print("##########################")



##########################
###-1778-6F2-Cell-detailed
##00 df b3 f6 dc 3d 6f cf
##01 d9 73 f5 fc 3d 6b cf
##02 da 73 f6 ac 3d 6b cf
##03 da 33 f6 ac 3d 63 cf
##04 d8 73 f6 1c 3d 33 cf
##05 cc b3 f3 fc 3c 37 cf
##06 e5 33 f8 4c 3e 8b cf
##07 e4 f3 f8 8c 3e 93 cf
##08 e5 33 f9 8c 3e 9b cf
##09 df b3 f6 ec 3d 77 cf
##0a de b3 f7 2c 3d 43 cf
##0b d1 73 f4 0c 3d 3b cf
##0c d6 f3 f4 5c 3d 53 cf
##0d d7 f3 f5 8c 3e 97 cf
##0e e9 33 fa 8c 3e a7 cf
##0f e0 f3 f7 fc 3d 7b cf
##10 df b3 f7 3c 3e 8b cf
##11 df 33 f8 1c 3e 7f cf
##12 e1 33 f8 2c 3e 77 cf
##13 dd 73 f7 0c 3e 7f cf
##14 df b3 f7 fc 3d 7b cf
##18 ca 83 fd a0 3c 10 10
##19 c2 c3 fd d0 3c f8 0f
##1a d0 43 fc 10 3d dc 0f
##1b b1 83 f8 30 3c 84 0f
##1c cc c3 ff 10 3c dc 0f
##1d cd 43 fb b0 3c d4 0f
##1e d1 03 fe 80 3c c4 0f
##########################
"""ettsjusjuatta = {
    0x01, 0xd9, 0x73, 0xf5, 0xfc, 0x3d, 0x6b, 0xcf,
    0x02, 0xda, 0x73, 0xf6, 0xac, 0x3d, 0x6b, 0xcf,
    0x03, 0xda, 0x33, 0xf6, 0xac, 0x3d, 0x63, 0xcf,
    0x04, 0xd8, 0x73, 0xf6, 0x1c, 0x3d, 0x33, 0xcf,
    0x05, 0xcc, 0xb3, 0xf3, 0xfc, 0x3c, 0x37, 0xcf,
    0x06, 0xe5, 0x33, 0xf8, 0x4c, 0x3e, 0x8b, 0xcf,
    0x07, 0xe4, 0xf3, 0xf8, 0x8c, 0x3e, 0x93, 0xcf,
    0x08, 0xe5, 0x33, 0xf9, 0x8c, 0x3e, 0x9b, 0xcf,
    0x09, 0xdf, 0xb3, 0xf6, 0xec, 0x3d, 0x77, 0xcf,
    0x0a, 0xde, 0xb3, 0xf7, 0x2c, 0x3d, 0x43, 0xcf,
    0x0b, 0xd1, 0x73, 0xf4, 0x0c, 0x3d, 0x3b, 0xcf,
    0x0c, 0xd6, 0xf3, 0xf4, 0x5c, 0x3d, 0x53, 0xcf,
    0x0d, 0xd7, 0xf3, 0xf5, 0x8c, 0x3e, 0x97, 0xcf,
    0x0e, 0xe9, 0x33, 0xfa, 0x8c, 0x3e, 0xa7, 0xcf,
    0x0f, 0xe0, 0xf3, 0xf7, 0xfc, 0x3d, 0x7b, 0xcf,
    0x10, 0xdf, 0xb3, 0xf7, 0x3c, 0x3e, 0x8b, 0xcf,
    0x11, 0xdf, 0x33, 0xf8, 0x1c, 0x3e, 0x7f, 0xcf,
    0x12, 0xe1, 0x33, 0xf8, 0x2c, 0x3e, 0x77, 0xcf,
    0x13, 0xdd, 0x73, 0xf7, 0x0c, 0x3e, 0x7f, 0xcf,
    0x14, 0xdf, 0xb3, 0xf7, 0xfc, 0x3d, 0x7b, 0xcf,
    0x18, 0xca, 0x83, 0xfd, 0xa0, 0x3c, 0x10, 0x10,
    0x19, 0xc2, 0xc3, 0xfd, 0xd0, 0x3c, 0xf8, 0x0f,
    0x1a, 0xd0, 0x43, 0xfc, 0x10, 0x3d, 0xdc, 0x0f,
    0x1b, 0xb1, 0x83, 0xf8, 0x30, 0x3c, 0x84, 0x0f,
    0x1c, 0xcc, 0xc3, 0xff, 0x10, 0x3c, 0xdc, 0x0f,
    0x1d, 0xcd, 0x43, 0xfb, 0xb0, 0x3c, 0xd4, 0x0f,
    0x1e, 0xd1, 0x03, 0xfe, 0x80, 0x3c, 0xc4, 0x0f,

}"""

ettsjusjuatta = ([0x00, 0xdf, 0xb3, 0xf6, 0xdc, 0x3d, 0x6f, 0xcf])


def lineindex():
    return ettsjusjuatta[0]
def linevalue():
    return ettsjusjuatta[0-8] >= 8
def allt():
    return ettsjusjuatta[0-8]

tempindex = (lineindex() * 4) -95
cellindex = (lineindex()*4+1)

isvoltage = False

if  lineindex() < 24:
    isvoltage = True

for i in range(4):
    if isvoltage:
        vol = allt() & 0x3FFF;
        cell = cellindex * 0.000305
        print(cell)



print(isvoltage)
print(linevalue())


print(tempindex)
print(lineindex())




"""
  uint8_t index=My6F2data.byte[0]; //Get our line index from byte 0;
	tempindex=(index*4)-95;          //Determine where these two messages fit in array based on index.
	cellindex=index*4+1;
  isVoltage = false;
  if (My6F2data.byte[0] < 24) isVoltage = true;  //First 24 messages (0-23) are voltage.  The rest are temp.

   My6F2data.value >>= 8; //skip over the counter byte

   for(int i=0;i<4;i++)  //We should have four 14-bit values
   {
      if(isVoltage)
      {
        vol=My6F2data.value&0x3FFF; //copy off 14 rightmost bits as an unsigned voltage.
        cell[cellindex++]=(vol*0.000305); //Correct voltage for scale and cast to float
      }
      else //This is a temp
      {
        tem=My6F2data.value&0x3FFF; //copy off 14 rightmost bits as a signed temperature.
        tem = (tem & 0x1FFF) - (tem & 0x2000); //Take 13 data bits and subtract 14th sign bit forcing it to bit 16
                                               //This casts a 14bit signed value to a 16 bit value preserving sign.
        temp[tempindex++]=tem*0.0122;  //Correct temperature for scale and cast result into float
      }
      My6F2data.value >>= 14; //shift away this 14 bit signed integer to access next value
    }

   int i=1;
   for(int j=1; j<17;j++)
   {
    module[j]=0.0f;
    module[j]=module[j]+cell[i++]+cell[i++]+cell[i++]+cell[i++]+cell[i++]+cell[i++];
   }

   voltage=0.0f;
  for(int j=1; j<17;j++)
   {
    voltage+=module[j];
   }

   averagetemp=0.0f;
    for(int j=1; j<33;j++)
   {
    averagetemp+=temp[j];
   }
   averagetemp/=32.0f;

}

float msgID6F2::getVoltage()
{
   return voltage;
}

float msgID6F2::getCell(int index)
{
   if(index<1||index>96)return -1;
   else return cell[index];
}

float msgID6F2::getTemp(int index)
{
  if(index<1||index>32)return -1;
   else return temp[index];
}

float msgID6F2::getModule(int index)
{
  if(index<1||index>16)return -1;
  else return module[index];
}"""