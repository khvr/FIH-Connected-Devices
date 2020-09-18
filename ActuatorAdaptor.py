'''
Created on Apr 15,2019

@author: hkalyan
'''

from project import ActuatorData
from project import SenseHatLedActivator
from project import SmtpClientConnector

'''
ActuatorAdaptor - class to process actuator message, update it and set message to SenseHat

@var ActuatorData: instance of ActuatorData class
@var SenseHatLedActivator: instance of SenseHatLedActivator class
'''
class ActuatorAdaptor(object):
    
    ActuatorData = None
    SenseHatLedActivator = None
    
    '''
    ActuatorAdaptor Constructor
    '''
    def __init__(self):
       
        self.ActuatorData = ActuatorData.ActuatorData()
        self.connector = SmtpClientConnector.SmtpClientConnector()
        self.SenseHatLedActivator = SenseHatLedActivator.SenseHatLedActivator()
        self.SenseHatLedActivator.setEnableLedFlag(True)    #Enable the SenseHatLedActivator Thread
        self.SenseHatLedActivator.start()   #Start the SenseHatLedActivator Thread

    '''
    function to process ActuatorData, update it and set message to SenseHat
    
    @param key: key which is passed to trigger the corresponding actuator based
    on the provided switching logic
    @param ActuatorData: ActuatorData that needs to be processed
    '''
    def processMessage(self, key, ActuatorData):
        
        if (key != None):
            if(self.ActuatorData != ActuatorData):
                if (key == "thermostat"):
                    self.SenseHatLedActivator.setDisplayMessage('temperature set to ' + str(ActuatorData.thermostat) + ' ˚C ');
                    self.connector.publishMessage('**************Temperature is not Feasible**************** ' , 'setting temperature to' + str(abs(ActuatorData.thermostat)) + ' ˚C ')
                elif(key == "sprinklers"):
                    self.SenseHatLedActivator.setDisplayMessage('pressure set to ' + str(ActuatorData.sprinklers));
                    self.connector.publishMessage('**************Smoke Detected********************' , 'starting sprinklers ' + str(abs(ActuatorData.sprinklers)))
                elif(key == "humidifier"):
                    self.SenseHatLedActivator.setDisplayMessage('humidity set to ' + str(ActuatorData.humidifier) + ' RH ');
                    self.connector.publishMessage('**************Humidity is not Feasible****************', 'setting humidity to ' + str(abs(ActuatorData.humidifier)) + ' RH ')
        self.ActuatorData.updateData(ActuatorData)