from machine import Pin
import utime

LONGPRESSTIME = 1000

# button class
class Button:
    def __init__(self, pin):
        self.pin = pin
        self.risingFlag = 0
        self.debounceTime = 0  # timestamp
        self.pressStartTime = 0
        self.longPressFlag = 0
        # Detection de front montant du bouton
        self.pin.irq(trigger=self.pin.IRQ_RISING, handler=self.callbackEdge)
    

    def callbackEdge(self, pin):
        currentTime = utime.ticks_ms()
        
        if utime.ticks_diff(current_time, self.debounceTime) > 100:
            self.debounceTime = current_time
            self.risingFlag = 1
            # utiliser pour long press
            self.pressStartTime = current_time
        
    def risingTreated(self):
        self.risingFlag = 0
        
    def rising(self):
        if self.risingFlag == 1:
            return 1
        else:
            return 0
    def pressed(self):
        if self.pin.value() == 1:
            return 1
        else:
            return 0
        
    def checkLongPress(self):
        if self.pressed():
            currentTime = utime.ticks_ms()
            
            if utime.ticks_diff(currentTime, self.pressStartTime) > LONGPRESSTIME:
                if self.longPressFlag == 0:
                    # autre actions?
                    self.longPressFlag = 1
                return 1
        else:
            self.longPressFlag = 0;
        return 0
    
        

        
        
        
    