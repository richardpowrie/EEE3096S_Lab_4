##############################################################################
#EEE3096S lab 4
#Group 2A
#David Fransch (FRNDAV011)
#Richard Powrie (PWRRIC001)
#due 7 AUG 2018
##############################################################################

import RPi.GPIO as GPIO
import time

##############################################################################
#Define
##############################################################################
####BCM numbering
#switches
button1  = 4 #reset
button2  = 14 #frequency
button3  = 15 #stop
#button4  = 18 #display

#ADC
SCLK     = 11#connected to ADC pin 13
MOSI     = 10#connected to ADC pin 11
MISO     = 9 #connected to ADC pin 12
ADCselect= 25#select ADC by pulling low, default high for no comms
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

#frequencies
f1       = 2   #every 500ms
f2       = 1   #every second
f3       = 0.5 #every 2s

#output
outHeading = "Time      Timer     Pot    Temp  Light\n"#format: 2 spaces between columns
outLines   = "--------------------------------------"
outString  = outHeading+outLines
##############################################################################


##############################################################################
#GPIO setup
##############################################################################
#use GPIO BCM pin numbering
GPIO.setmode(GPIO.BCM)              
#outputs

#set up buttons as digital inputs, using pull-up resistors
GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

##############################################################################


##############################################################################
#main
##############################################################################
print(outString)
#release GPIO pins from operation
GPIO.cleanup()
##############################################################################
