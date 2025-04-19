from machine import Pin, I2C
import utime
# pour ce projet il faut importer une librairie pour l'écran
# Tools -> Manage packages -> micropython-ssd1306 (ecran)
# Tools -> Manage packages -> micropython-oled (pour changer les grosseurs des texts)
from ssd1306 import SSD1306_I2C
from oled import Write, GFX, SSD1306_I2C
from oled.fonts import ubuntu_mono_15, ubuntu_mono_20 # juste deux fonts different

# Pins utilisees:
led = Pin(25, Pin.OUT)
switch = Pin(14, Pin.IN, Pin.PULL_DOWN)
screen_SCL = Pin(17)
screen_SDA = Pin(16)

# Screen variables
WIDTH = 128
HEIGHT = 32

###########################################################
# Init
###########################################################

# Set I2C connection for screen
i2c = I2C(0, scl=screen_SCL, sda=screen_SDA, freq=400000)

# Connection test / Init
devices = i2c.scan()
print("I2C devices:", devices)
# Set screen object
if len(devices) == 0:
    print("No I2C device found!")
else:
    oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)
    oled.fill(0)

###########################################################
# Fonctions
###########################################################
def welcome_message():
    oled.text('Projet par:', 0, 0)
    oled.text('Charles-A Dion', 0, 10)
    oled.text('Jacob Turcotte', 0, 20)
    oled.show()

def clear_screen():
    # Function to earse the screan content
    oled.fill(0)
    oled.show()
    
def show_screen():
    oled.show()
    
def write15(text, x, y):
    write15 = Write(oled, ubuntu_mono_15)
    write15.text(text, y, x)
    show_screen();
    
def write20(text, x, y):
    write20 = Write(oled, ubuntu_mono_20)
    write20.text(text, y, x)
    show_screen();

###########################################################
# Main Code
###########################################################

# Welcome message
welcome_message()
utime.sleep_ms(2000)
clear_screen()

# Test de class 

# Main loop
while True:
    if (switch.value() == 1):
        led.value(1)
        write15("tricky", 0, 0)
    else:
        led.value(0)
        clear_screen()
        
    utime.sleep_ms(1)

    
    
  
  
  
  
  
  
  