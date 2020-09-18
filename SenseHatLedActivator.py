'''
Created on Feb 1, 2019

@author: hkalyan
'''

from time import sleep
from sense_hat import SenseHat
import threading

'''
SenseHatLedActivator : SenseHat activator class for LED to show message

@param enableLed: to enable LED display thread
@param rateInSec: LED display rate
@param rotateDeg: angle of display
@param sh: instance of SenseHat
@param displayMsg: Message to display
'''
class SenseHatLedActivator(threading.Thread):
  
    enableLed = False
    rateInSec = 1
    rotateDeg = 270
    sh = None
    displayMsg = None
     
    '''
    SenseHatLedActivator constructor
    
    @param rotateDeg: angle of rotation in degree
    @param rateInSec: time in seconds
    '''
    def __init__(self, rotateDeg = 270, rateInSec = 1):
       
        super(SenseHatLedActivator, self).__init__()
        
        if rateInSec > 0:
            self.rateInSec = rateInSec
        if rotateDeg >= 0:
            self.rotateDeg = rotateDeg

        self.sh = SenseHat()
        self.sh.set_rotation(self.rotateDeg)
         
    '''
    SenseHatLedActivator thread function
    '''
    def run(self):
        
        while True:
            if self.enableLed:
                if self.displayMsg != None:
                    self.sh.show_message(str(self.displayMsg))  #show scrolling LED message
                else:
                    #self.sh.show_letter(str('R'))
                    self.sh.show_letter('')
    
                sleep(self.rateInSec)
                self.sh.clear()

            sleep(self.rateInSec)
     
    '''
    function to get display rate
    
    @return: 'rateInSec' - time in seconds
    '''
    def getRateInSeconds(self):
       
        return self.rateInSec
 
    '''
    function to enable LED display
    
    @param enable: True, to set the LED flag else False 
    '''
    def setEnableLedFlag(self, enable):
        
        self.sh.clear()
        self.enableLed = enable
     
    '''
    function to set the message to be displayed in LED
    
    @param msg: String message to be displayed
    '''
    def setDisplayMessage(self, msg):
       
        self.displayMsg = msg