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

# Time varaibles
INACTION_TIME = 10000


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
        utime.sleep_ms(4000)
        currentScreen = 'idle'
        screen.clear()
        lastActiontime = utime.ticks_ms()
        # working loop : screen navigation logic: 
        while True:
            currentTime = utime.ticks_ms()
            #print(['active screen is: ', currentScreen])
            #print(['temps depuis action: ', str(lastActiontime), 'temps actuel: ', str(currentTime), 'comparaison: ', str(utime.ticks_diff(currentTime, lastActiontime))])
            if currentScreen == 'idle':
                lastActiontime = utime.ticks_ms()
                screen.showIdle()
                if button.press():
                    button.treated()
                    screen.clear()
                    currentScreen = 'request work'
                elif button.longPress():
                    button.treated()
                    screen.clear()
                    currentScreen = 'all params'
                    
            # **************
            # Params section
            # **************
            # si no action time est depasser retourne a idle:
            
            elif ((currentScreen == 'all params') | (currentScreen == 'param' )) & (utime.ticks_diff(currentTime, lastActiontime) > INACTION_TIME):
                screen.clear()
                currentScreen = 'idle'
            
            # menus de params:
            elif  currentScreen == 'all params':
                screen.showMenu()
                if button.press():
                    button.treated()
                    lastActiontime = utime.ticks_ms()
                    screen.incrementCursor()
                elif button.longPress():
                    button.treated()
                    lastActiontime = utime.ticks_ms()
                    screen.clear()
                    currentScreen = 'param'
                    
            # sous-menu de param:        
            elif currentScreen == 'param':
                screen.showSubMenu()
                if button.press():
                    button.treated()
                    lastActiontime = utime.ticks_ms()
                    screen.incrementSubMenu()
                elif button.longPress():
                    button.treated()
                    lastActiontime = utime.ticks_ms()
                    screen.clear()
                    currentScreen = 'all params'
            
            # **************
            # work screens section
            # **************
            
            # starting work session
            elif currentScreen == 'request work':
                #print('request start catch')
                screen.showRequestStart()
                if button.press():
                    button.treated()
                    workModeStart = utime.ticks_ms()
                    screen.clear()
                    currentScreen = 'work mode'
                    
                elif button.longPress() | (utime.ticks_diff(currentTime, lastActiontime) > INACTION_TIME): # si on pese pendant longtemps ou on fait rien pendant longtemps on reviens a idle
                    button.treated()
                    lastActiontime = utime.ticks_ms()
                    screen.clear()
                    currentScreen = 'idle'
            
            # work mode screen         
            elif currentScreen == 'work mode':
                screen.showWorkMode(utime.ticks_diff(currentTime, workModeStart))
                if button.press() | (utime.ticks_diff(currentTime, workModeStart) > screen.getWorkTime()): # si temps est ecouler ou on pese pour skip
                    button.treated()
                    lastActiontime = utime.ticks_ms()
                    screen.clear()
                    currentScreen = 'request break'
                    
                elif button.longPress():
                    button.treated()
                    lastActiontime = utime.ticks_ms()
                    screen.clear()
                    currentScreen = 'request give up'
            
            # break mode requested
            elif currentScreen == 'request break':
                screen.showRequestBreak()
                if button.press():
                    button.treated()
                    chillModeStart = utime.ticks_ms()
                    screen.clear()
                    screen.incrementCompletedWorkSessions()
                    currentScreen = 'break mode'
                elif (button.longPress() | utime.ticks_diff(currentTime, lastActiontime) > INACTION_TIME) & (utime.ticks_diff(currentTime, workModeStart) < screen.getWorkTime()): # si temps est pas finit et tu pese le bouton longtemps ou inaction 
                    button.treated()
                    lastActiontime = utime.ticks_ms()
                    screen.clear()
                    currentScreen = 'work mode' # retourne au work mode si pas finit le tps
            
            # break mode
            elif currentScreen == 'break mode':
                screen.showChillMode(utime.ticks_diff(currentTime, chillModeStart))
                if button.press() | (utime.ticks_diff(currentTime, chillModeStart) > screen.getChillTime()): # si tps finit ou on skip 
                    button.treated()
                    lastActiontime = utime.ticks_ms()
                    screen.clear()
                    currentScreen = 'request work'
                    
                elif button.longPress():
                    button.treated()
                    lastActiontime = utime.ticks_ms()
                    # fait rien pour linstant mais pourrais implementer puisse give up ici
                    #screen.clear()
                    #currentScreen = 'request give up'
            
        
            # give up screen
            elif currentScreen == 'request give up':
                screen.showRequestGiveUp()
                if button.press():
                    button.treated()
                    lastActiontime = utime.ticks_ms()
                    screen.clear()
                    currentScreen = 'idle'
                    
                elif button.longPress():
                    button.treated()
                    lastActiontime = utime.ticks_ms()
                    screen.clear()
                    currentScreen = 'work mode'
            
                    
            
            
            # slow down screen for easier debug 
            utime.sleep_ms(200)
            
            
            
    else:
        print(' Communication failed, retrying in 5 seconds')
        utime.sleep_ms(5000)
        
        
        
        
#Code test pour les boutons
'''
            # update light
            if button.press():
                print('button pressed')
                button.treated()
                
                led.value(1)
                
            elif button.longPress():
                print('button longpressed')
                button.treated()
                
                led.value(0)

'''
  
  
  
  
  
  