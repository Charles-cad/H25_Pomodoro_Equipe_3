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
        
        # variables pour les parametres:
        self.workTime = 25
        self.shortChillTime = 5
        self.longChillTime = 30
        self.orientation = 0
        # Variable pour le curseur:
        self.cursor = 0
        # conteurs de work sessions
        self.completedWorkSessions = 0 # 0 a 4 fait 5 session de travail
        # variable pour savoir les changmenet de temps afin de pas spam le refresh rate
        self.oldtimeLeft = 'timex'
                
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
    
    def smallText(self, message = '-', line = 0, colomn = 0):
        caracterSize = 8
        posY = caracterSize * line
        posX = caracterSize * colomn
        self.screen.text(message, posX, posY)
        self.screen.show();
        
    def mediumText(self, message = '-', line = 0, colomn = 0):
        caracterSize = 15
        posY = caracterSize * line
        posX = caracterSize * colomn
        write15 = Write(self.screen, ubuntu_mono_15)
        write15.text(message, posX, posY)
        self.screen.show();
    
    def largeText(self, message = '-', line = 0, colomn = 0):
        caracterSize = 20
        posY = caracterSize * line
        posX = caracterSize * colomn
        write = Write(self.screen, ubuntu_mono_20)
        write.text(message, posX, posY)
        self.screen.show();
        
    def text(self, message = '-', line = 0, colomn = 0, size = 8):
        if size <= 8:
            size = 8
        elif size > 8 & size <= 15:
            size = 15    
        else:
            size = 20
            
        if size == 8:
            self.smallText(message, line, colomn)
        elif size == 15:
            self.mediumText(message, line, colomn)
        elif size == 20:
            self.largeText(message, line, colomn)
        else:
            print('invalid size')
            return 99 #problem! invalid
        return 1
    
    def welcomeMessage(self):
        self.text('Pomodoro C3I')
        self.text('Projet par:   ', 1)
        self.text('Charles-A Dion', 2)
        self.text('Jacob Turcotte', 3)
        
##############################################   
# creations des differentes pages :
##############################################
    ##############################################
    # Home screen
    ##############################################
    def showIdle(self):
        self.clear()
        #self.text('debug: idle')
    
    ##############################################
    # PARAMS screen
    ##############################################
    
    def showMenu(self):
        self.writeCursor()
        self.text('work time', 0, 2)
        self.text('short chill', 1, 2)
        self.text('long chill', 2, 2)
        self.text('orientation', 3, 2)
        
    def showSubMenu(self):
        selectedMenu = self.cursor
        subMenuText = ['work time: ','short chill time:','long chill time:','orientation:']
        self.text(subMenuText[selectedMenu], 0, 0, 15)
        
        # afficahge de la valeur
        subMenuValues = [str(self.workTime), str(self.shortChillTime), str(self.longChillTime), str(self.orientation) ]
        self.text(subMenuValues[selectedMenu], 1, 0, 15)
        
    def incrementSubMenu(self):
        #print('incrementeing param values')
        selectedMenu = self.cursor
        if selectedMenu == 0:
            self.workTime = self.workTime + 1
            if self.workTime > 30:
                self.workTime = 20
        elif selectedMenu == 1:
            self.shortChillTime = self.shortChillTime + 1
            if self.shortChillTime > 10:
                self.shortChillTime = 5
        elif selectedMenu == 2:
            self.longChillTime = self.longChillTime + 1
            if self.longChillTime > 30:
                self.longChillTime = 20
        elif selectedMenu == 3:
            self.orientation = self.orientation + 1
            if self.orientation > 1:
                self.orientation = 0
            if self.orientation == 0:
                self.screen.write_cmd(0xA1) 
                self.screen.write_cmd(0xC8)  # Vertical flip
            else:
                self.screen.write_cmd(0xA0)
                self.screen.write_cmd(0xC0)  # Normal
        self.clear()
        # cursor
    def writeCursor(self):
        self.text('->', self.cursor)
        
    def incrementCursor(self):
        self.cursor = self.cursor + 1
        if self.cursor > 3:
            self.cursor = 0
        self.clear()
        
        
        
    ##############################################
    # Main working mode section
    ############################################## 
        
    def showRequestStart(self):
        self.text('READY TO START?!')
        
    def showWorkMode(self, currentTime):
        # show time
        timeLeft = self.getTimeFormat(currentTime, self.getWorkTime())
        if not (timeLeft == self.oldtimeLeft):
            self.screen.fill(0)
            self.text('Work mode', 0, 0, 15)
            self.oldtimeLeft = timeLeft
            self.text(f"Time left: {timeLeft}", 1, 0, 15)
            
        
    def showRequestBreak(self):
        self.text('GOOD WORK!', 0, 0, 20)
        self.text('Break time?', 1, 0, 20)
        
    def showChillMode(self, currentTime):
        # afficahge du temps
        timeLeft = self.getTimeFormat(currentTime, self.getChillTime())
        if not (timeLeft == self.oldtimeLeft):
            self.screen.fill(0)
            self.text('Time to chill', 0, 0, 15)
            self.oldtimeLeft = timeLeft
            self.text(f"Time left: {timeLeft}", 1, 0, 15)
        
    def getTimeFormat(self, currentTime, maxTime):
        timeLeft = max(0, maxTime - currentTime) # affiche pas de negatifs
        # conversion en secondes
        totalSeconds = timeLeft // 1000
        minutes = totalSeconds // 60
        seconds = totalSeconds % 60 
        
        # conversion dans le bon format
        timeStr = f"{minutes:02}:{seconds:02}" # affichage sur 2 chiffre
        return timeStr
    
    def showRequestWork(self):
        self.text('Ready to work?',  0, 0, 20)
    
    def showRequestGiveUp(self):
        self.text('Quitting?', 0, 0, 20)
        self.text('You sure?', 1, 0, 20)
      
    
    # management des work sessions
    
    def incrementCompletedWorkSessions(self):
        self.completedWorkSessions = (self.completedWorkSessions + 1)
        if self.completedWorkSessions > 4:
            self.completedWorkSessions = 0
    
    def getWorkTime(self):
        return (self.workTime * 60 * 1000)
    def getChillTime(self):
        if self.completedWorkSessions >= 4:
            return (self.longChillTime * 60 * 1000)
        else:
            return (self.shortChillTime * 60 * 1000)
        
        
        
        
        
        
        