##############################################################################
#EEE3096S lab 4
#Group 2A
#David Fransch (FRNDAV011)
#Richard Powrie (PWRRIC001)
#due 7 AUG 2018
##############################################################################

import RPi.GPIO as GPIO
import time

import spidev
import os
import sys

##############################################################################
#Define
##############################################################################
####BCM numbering
#switches
button1  = 4  #reset
button2  = 14 #frequency
button3  = 15 #stop
button4  = 18 #display

#ADC
SPICLK   = 11          #connected to ADC pin 13
SPIMOSI  = 10          #connected to ADC pin 11
SPIMISO  = 9           #connected to ADC pin 12
SPICS    = 8           #select ADC by pulling low, default high for no comms
"""ADC set up as follows:
Channel Peripheral ADC pin Selection bits
CH0     Pot        1       1000
CH1     Thermistor 2       1001
CH2     LDR        3       1010
   Set up in single ended mode (common ground between them)
DGND    GND        9
   connected to ground
   http://www.hit.bme.hu/~papay/edu/Acrobat/GndADCs.pdf explains why they're connected together
CS/SHDN ADCselect  10
   selected by pulling low
Din     MOSI       11
Dout    MISO       12
CLK     SCLK       13
AGND    GND        14
   connected to ground
VREF    3v3        15
   equation: V_in = digital_output_code*V_ref/1024
                  = digital_output_code*3.3/1024
VDD     3v3        16
"""
#channels
pot = 0
therm = 1
LDR = 2

#frequencies
t1       = 0.5   #every 500ms
t2       = 1   #every second
t3       = 2 #every 2s

#output
outHeading = "Time      Timer     Pot    Temp  Light\n"#format: 2 spaces between columns
outLines   = "--------------------------------------"
outString  = outHeading+outLines

decimal_places = 3


##############################################################################
#SPI setup
##############################################################################
spi = spidev.SpiDev()
spi.open(0,0)#bus #0 and device #0
spi.max_speed_hz=1000000


##############################################################################
GPIO setup
##############################################################################
#use GPIO BCM pin numbering
GPIO.setmode(GPIO.BCM)              
#outputs
GPIO.setup(SPIMOSI,GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

#set up buttons as digital inputs, using pull-up resistors
GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

##############################################################################
#functions
##############################################################################
def GetData(channel):#channel = integer 0-7
    adc = spi.xfer2([1,(8+channel)<<4,0])#send three bits with single ended mode selected
    data = ((adc[1]&3)<<8) + adc[2]
    return data

# function to convert data to voltage level, 
# places: number of decimal places needed 
def ConvertVolts(data,places): 
    volts = (data * 3.3) / float(1023)
    volts = round(volts,places)
    return volts
    

def convertTemp(data, places):
    temp = (data-0.5)/0.010
    #temp = ((data*330)/float(1023))-50
    temp = round(temp,places)
    return temp

#threaded callbacks
def callback1(button1):#reset
    global timerStart
    timerStart = time.time()#reset timer
    os.system("clear")
	print("Reset pressed")
    print(outString)
    
def callback2(button2):#frequency
    global delay
    if delay==t1:
        delay=t2
    elif delay==t2:
        delay=t3
    else:
        delay=t1
	print("new sample time:"+str(delay))

GPIO.add_event_detect(button1, GPIO.FALLING, callback=callback1,bouncetime=400)
GPIO.add_event_detect(button2, GPIO.FALLING, callback=callback2,bouncetime=400)
    
##############################################################################
#main
##############################################################################
print(outString)

delay = t1
timerStart = time.time()
while True:
    try:
        #read pot
        pot_data = GetData(pot)
        Vpot = ConvertVolts(pot_data,decimal_places)
        #read temp
        therm_data = GetData(therm)
        Vtherm = ConvertVolts(therm_data,decimal_places)
        AmbTemp = convertTemp(Vtherm,decimal_places)
        #read light
        LDR_data = GetData(LDR)
        LDRper = ConvertVolts(LDR_data,decimal_places)/3.11*100
        
        #create output string
        currentTime = time.strftime("%H:%M:%S",time.localtime())        
        timer = time.strftime("%H:%M:%S",time.gmtime(time.time()-timerStart))
        output_string = currentTime + "  " + timer+"  " +("%3.1f V" % Vpot)+ "  " + ("%2.0f C" % AmbTemp)+ "  " + ("%2.0f%%" % LDRper)
        print(output_string)
        
        #delay
        time.sleep(delay)
        
    except KeyboardInterrupt:
        spi.close()
        break
        
#release GPIO pins from operation
#GPIO.cleanup()
