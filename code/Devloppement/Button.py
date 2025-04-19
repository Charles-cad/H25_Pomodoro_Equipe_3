from machine import Pin
import utime

LONG_PRESS_TIME = 1000
DEBOUNCE_TIME = 100

# button class
class Button:
    def __init__(self, pin):
        self.pin = pin
        self.debounceTime = 0  # timestamp pour savoir quand etais la derniere action
        self.pressTime = 0 # temps quand on appui
        self.releaseTime = 0 # temps quand on release
        self.pressFlag = 0 # flag pour dire quon a peser rapidement
        self.longPressFlag = 0 # flag pour dire quon a maintenu le bouton pendant longtemps
        
        # Detection de front montant du bouton
        self.pin.irq(trigger=self.pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.callbackEdge)
    

    def callbackEdge(self, pin):
        currentTime = utime.ticks_ms()
        if utime.ticks_diff(currentTime, self.debounceTime) < DEBOUNCE_TIME:
            return # si < debounce time on ignore
        self.debounceTime = currentTime
        
        if self.pressed() == 1:  # Bouton pressé 
            self.pressTime = currentTime
        else:
            self.releaseTime = currentTime
            press_duration = utime.ticks_diff(self.releaseTime, self.pressTime)
            
            if press_duration >= LONG_PRESS_TIME:
                self.longPressFlag = 1
            else:
                self.pressFlag = 1
        
    def pressed(self):
        if self.pin.value() == 1:
            return 1
        else:
            return 0
        
    def press(self):
        return self.pressFlag == 1
        
    def longPress(self):
        return self.longPressFlag == 1
    
    def treated(self):
        self.pressFlag = 0
        self.longPressFlag = 0
    
        

        
        
        
    