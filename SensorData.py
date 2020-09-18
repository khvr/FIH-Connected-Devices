
'''
Created on Jan 25, 2019

@author: hkalyan
'''

import os
from datetime import datetime

'''
SensorData - class to calculate and categorize required value from sensor data.

@var tempsensor: the tempsensor value passed
@var humidsensor: the humidsensor value passed
@var smokesensor: the smokesensor value passed
'''
class SensorData(object):
    
    tempsensor = 0
    humidsensor = 0
    smokesensor = 0
    
    '''
    SensorData constructor
    '''
    def __init__(self):
        
        self.timeStamp = str(datetime.now())
        self.totValue = [0, 0, 0]
        self.avgValue = [0, 0, 0]
        self.sampleCount = 0
        
    '''
    calculates and categorizes required values from sensor readings.
    
    @param newVal: new sensor value.
    '''
    def addValue(self, newVal):
      
        print('\n--------------------')
        print('Sensor readings : ' + str(newVal) )
        
        self.sampleCount += 1
        self.timeStamp = str(datetime.now())
        self.tempsensor = newVal[0]
        self.smokesensor = newVal[1]
        self.humidsensor = newVal[2]
        self.totValue[0] += newVal[0]
        self.totValue[1] += newVal[1]
        self.totValue[2] += newVal[2]
        

        i = 0
        for x in self.totValue :
            if (x != 0 and self.sampleCount > 0):
                self.avgValue[i] = (x / self.sampleCount)
            i += 1

    '''
    returns the string representation of the SensorData object.
    
    @return: 'customStr' - SensorData object in string.
    '''
    def __str__(self):
      
        customStr = \
        os.linesep + '\ttimeStamp: ' + self.timeStamp + \
        os.linesep + '\ttempsensor: ' + str(self.tempsensor) + \
        os.linesep + '\tsmokesensor: ' + str(self.smokesensor) + \
        os.linesep + '\thumidsensor: ' + str()
        
        return customStr