# C3I H25 projet POMODORO
# Charles-Ariel Dion
# 18-4-2025
# fichier de classe pour ecran oled 0.91''


# tous les imports :
from machine import Pin, I2C
# pour ce projet il faut importer une librairie pour l'écran
# Tools -> Manage packages -> micropython-ssd1306 (ecran)
# Tools -> Manage packages -> micropython-oled (pour changer les grosseurs des texts)
from ssd1306 import SSD1306_I2C
from oled import Write, GFX, SSD1306_I2C
from oled.fonts import ubuntu_mono_15, ubuntu_mono_20 # import deux fonts different

# example class
class TrafficLight:
    '''Traffic light class'''
    def __init__(self, color = 'red'):
        self.color = color
        
    def action(self):
        if self.color == 'red':
            print('stop')
        elif self.color == 'yellow':
            print('prepare to stop')
        elif self.color == 'green':
            print('go')
        else:
            print('stop drinking lol')
# test code for TrafficLight class
 #       galt = TrafficLight()
 #       galt.action()
 #       utime.sleep_ms(2000)
 #       galt.color = 'green'
 #       galt.action()
        
# Screen class
class OledScreen:
    '''Class for oled display, used with ssd1306 & oled libraries'''
    def __init__(self, width = 128, height = 32,  SCL = Pin(17), SDA = Pin(16), freq = 400000):
        self.height = height
        self.width = width
        self.SCL = SCL
        self.SDA = SDA
        self.freq = freq
        #self.startCommunication(self):
                
    def startCommunication(self, show=0):
        # set oled screen object from SSD1306_I2C 
        self.i2c = I2C(0, scl=self.SCL, sda=self.SDA, freq=self.freq)
        if self.communicationTest(show):
            if show:
                print('establishing connection')
            self.screen = SSD1306_I2C(self.width, self.height, self.i2c)
            if show:
                print('connection established')
            return 1
        else:
            return 0 # Problem!
   
    def communicationTest(self, show = 0):
        devices = self.i2c.scan()
        if len(devices) == 0:
            if show:
                print("No I2C device found!")
            return 0
        else:
            if show:
                print("I2C devices found:", devices)
            return 1       
    
    def clear(self):
        self.screen.fill(0)
        self.screen.show()
    
    def smallText(self, message = '-', posX = 0, posY = 0):
        self.screen.text(message, posX, posY)
        self.screen.show();
    
    def mediumText(self, message = '-', posX = 0, posY = 0):
        write15 = Write(self.screen, ubuntu_mono_15)
        write15.text(message, posX, posY)
        self.screen.show();
    
    def largeText(self, message = '-', posX = 0, posY = 0):
        write = Write(self.screen, ubuntu_mono_20)
        write.text(message, posX, posY)
        self.screen.show();
        
    def text(self, message = '-', posX = 0, posY = 0, size = 10):
        if size == 10:
            self.smallText(message, posX, posY)
        elif size == 20:
            self.mediumText(message, posX, posY)
        elif size == 30:
            self.largeText(message, posX, posY)
        else:
            print('invalid size')
            return 99 #problem! invalid
        return 1
    
    def welcomeMessage(self):
        size = 10
        self.text('Projet par:   ', 0,  0, size)
        self.text('Charles-A Dion', 0, 10, size)
        self.text('Jacob Turcotte', 0, 20, size)
        
        