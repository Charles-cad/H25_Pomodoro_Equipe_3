# Code pour C3I H25 projet POMODORO
# Charles-Ariel Dion
# 18-4-2025
import micropython
from machine import Pin, I2C
import utime
# Classe OledScreen
from OledScreen import OledScreen
from Button import Button
# Pins utilisees:
led = Pin(25, Pin.OUT)
switch = Pin(14, Pin.IN, Pin.PULL_DOWN)
screen_SCL = Pin(17)
screen_SDA = Pin(16)

# Button object
button = Button(switch)

# Screen object
width = 128
height = 32
screen = OledScreen(width, height, screen_SCL, screen_SDA)

# boutton


###########################################################
# Main Code
###########################################################

# Init ******************

print('Starting code')

# Main program 
while True:
    # start communication
    if screen.startCommunication(1):
        # Welcome message
        screen.welcomeMessage()
        utime.sleep_ms(2000)

        # working loop
        while True:
            # update light
            if (button.rising() == 1):
                print('rising edge')
                button.risingTreated()
                
                led.value(1)
                
            elif (button.falling() == 1):
                print('falling edge')
                button.fallingTreated()
                
                led.value(0)
                
            # screen logic
            
                
            # 100 ms refresh rate    
            utime.sleep_ms(100)
    else:
        print(' Communication failed, retrying in 5 seconds')
        utime.sleep_ms(5000)
        
        
    
    
  
  
  
  
  
  
  