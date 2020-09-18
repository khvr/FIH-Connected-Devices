'''
Created on Feb 16, 2019

@author: hkalyan
'''

import json
from project import SensorData
from project import ActuatorData

'''
DataUtil.py : Class to convert Sensor Data to json and vice versa. Also updates 
a new a Actuator Data value

@var sensorData: Sensor Data object
@var ActuatorData: Actuator Data object
@var sensorJSON: Sensor Data in JSON form
@var actuatorJSON: Actuator Data in JSON form
@var dict: JSON string
@var dSenseData: default Sensor Data
@var dActuateData: default Actuator Data
'''
class DataUtil(object):
   
    sensorData = None
    ActuatorData = None
    sensorJSON = None
    actuatorJSON = None
    dict = None
    key = None
    dSenseData = '{"timeStamp":"0", "tempsensor":"0", "pressure":"0", "humidity":"0"}'
    dActuateData = '{"timeStamp":"0", "thermostat":"0", "humidifier":"0", "sprinklers":"0"}'

    '''
    DataUtil Constructor
    '''
    def __init__(self):
        
        self.sensorData = SensorData.SensorData()
        self.sensorJSON = json.dumps(self.dSenseData)
        self.ActuatorData = ActuatorData.ActuatorData()
        self.actuatorJSON = json.dumps(self.dActuateData)
    
    '''
    Function to convert Sensor Data to JSON
    
    @param sensordata: Sensor Data object
    @return sensorJSON: sensorJSON JSON string on success, null on failure
    '''
    def toJsonFromSensorData(self, sensorData):
        
        self.dict = {}
        self.dict['tempsensor'] = sensorData.tempsensor
        self.dict['smokesensor'] = sensorData.smokesensor
        self.dict['humidsensor'] = sensorData.humidsensor
        self.sensorJSON = json.dumps(self.dict)
        if (self.sensorJSON != None):
            sOutfile = open('SensorDatatoJSON.txt', 'w')
            sOutfile.write(self.sensorJSON)
            return self.sensorJSON
        
        return None
    
    '''
    Function to convert JSON to Sensor data
    
    @param JSON: JSON string
    @return sensorData: Sensor Data object on success, null on failure
    '''
    def toSensorDataFromJson(self, JSON):
        
        self.dict = json.loads(JSON)
        if (self.dict != None):
            self.sensorData.tempsensor = self.dict['tempsensor']
            self.sensorData.smokesensor = self.dict['smokesensor']
            self.sensorData.humidsensor = self.dict['humidsensor']
            return self.sensorData
        
        return None
    
    '''
    Function to convert Actuator Data to JSON
    
    @param ActuatorData: Actuator Data object
    @return actuatorJSON: actuatorJSON JSON string on success, null on failure
    '''
    def toJsonFromActuatorData(self, ActuatorData):
      
        self.actuatorJSON = json.dumps(ActuatorData.__dict__)
        if (self.actuatorJSON != None):
            aOutfile = open('ActuatorDatatoJSON.txt', 'w')
            aOutfile.write(self.actuatorJSON)
            return self.actuatorJSON
        
        return None
    
    '''
    Function to convert JSON to Sensor data
    
    @param JSON: JSON string
    @return actuatorData: Sensor Data object on success, null on failure
    '''
    def toActuatorDataFromJson(self, JSON):
       
        self.dict = json.loads(JSON)
        if (self.dict != None):
            self.ActuatorData.timeStamp = self.dict["timeStamp"]
            self.ActuatorData.thermostat = self.dict["thermostat"]
            self.ActuatorData.humidifier = self.dict["humidifier"]
            self.ActuatorData.sprinklers = self.dict["sprinklers"]
            return self.ActuatorData
        
        return None
    
    '''
    Function to update the ActuatorData based on the passed topic and the 
    subscribed JSON data
    
    @param topic: The topic based on which a switching logic is coded to 
    generate actuator data
    @param JSON: JSON data passed from the cloud subscriber
    '''
    def updateActuatorData(self, topic, JSON):
        print('Inside updateActuatorData ' + topic +'JSON :' + JSON)
        self.dict = json.loads(JSON)
        self.key = self.parseTopic(topic)
        print('key is ' + self.key)
        if (self.key != None):
            if (self.key == "thermostat"):
                self.ActuatorData.thermostat = self.dict["value"]
            elif(self.key == "sprinklers"):
                self.ActuatorData.sprinklers = self.dict["value"]
            elif(self.key == "humidifier"):
                self.ActuatorData.humidifier = self.dict["value"]
                
        print(self.ActuatorData)
            
    '''
    parses and extracts the device label from the provided topic
    
    @param topic: topic provided to extract the last label value
    @return: returns the device-label which is used as a key
    '''
    def parseTopic(self, topic):
        
        return topic.rsplit('/', 1)[-1]