'''
Created on Apr 16, 2019

@author: hkalyan
'''

import os
from datetime import datetime

'''
ActuatorData - class defines the ActuatorData object of Actuator

@param thermostat: Temperature actuator data 
@param humidifier: humidity actuator data 
@param sprinklers: smoke actuator data 
'''
class ActuatorData(object):

    thermostat = 0
    humidifier = 0
    sprinklers = 0
    
    '''
    ActuatorData Constructor
    '''
    def __init__(self):
      
        self.updateTimeStamp()
        
    '''
    function to update the ActuatorData
    
    @param data: ActuatorData 
    '''
    def updateData(self, data):
       
        self.thermostat = data.thermostat
        self.humidifier = data.humidifier
        self.sprinklers = data.sprinklers

    '''
    function to update the date and time 
    '''
    def updateTimeStamp(self):
        
        self.timeStamp = str(datetime.now())

    '''
    returns the string representation of the ActuatorData object.
    
    @return: 'customStr' - ActuatorData object in string.
    '''
    def __str__(self):
     
        customStr = \
        os.linesep + '\ttimeStamp: ' + self.timeStamp + \
        os.linesep + '\tthermostat ' + str(self.thermostat) + \
        os.linesep + '\thumidifier: ' + str(self.humidifier) + \
        os.linesep + '\tsprinklers: ' + str(self.sprinklers)
        return customStr