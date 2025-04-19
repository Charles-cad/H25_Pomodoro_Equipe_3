# Code pour C3I H25 projet POMODORO
# Charles-Ariel Dion
# 18-4-2025

from machine import Pin, I2C
import utime
# Classe OledScreen
from OledScreen import OledScreen

# Pins utilisees:
led = Pin(25, Pin.OUT)
switch = Pin(14, Pin.IN, Pin.PULL_DOWN)
screen_SCL = Pin(17)
screen_SDA = Pin(16)
width = 128
height = 32
# Screen object
screen = OledScreen(width, height, screen_SCL, screen_SDA)

###########################################################
# Main Code
###########################################################

# Init ******************
print('Starting code')

# Main program 
while True:
    # start communication
    if screen.startCommunication(1):
        print('booting screen')
        # Welcome message
        screen.welcomeMessage()
        utime.sleep_ms(2000)
        print('screen booted')
        
        # working loop
        print('entering working loop')
        while True:
            
            if (switch.value() == 1):
                led.value(1)
                print('writting tricky')
                screen.text('tricky')
            else:
                led.value(0)
                screen.clear()
                
            # 100 ms refresh rate    
            utime.sleep_ms(100)
    else:
        print(' Communication failed, retrying in 5 seconds')
        utime.sleep_ms(5000)
        
    
  
  
  
  
  
  
  