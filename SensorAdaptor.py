'''
Created on Apr 15, 2019

@author: hkalyan
'''

import threading 
from project import SensorData
from project import ActuatorData
from project import ActuatorAdaptor
from sense_hat import SenseHat
from random import uniform
from time import sleep
from project import DataUtil
from project import MqttSubClient
from project import HTTPCloudPublisher

UBIDOTS_DEVICE_LABEL = "rbcloud"#making DEVICE_LABEL global variable
UBIDOTS_VARIABLE_TEMPERATURE_LABEL = "thermostat"#making TEMPERATURE_LABEL global variable
UBIDOTS_VARIABLE_SMOKE_LABEL = "sprinklers"#making SMOKE_LABEL global variable
UBIDOTS_VARIABLE_HUMIDITY_LABEL = "humidifier"#making HUMIDITY_LABEL global variable
UBIDOTS_VARIABLES = [UBIDOTS_VARIABLE_TEMPERATURE_LABEL, UBIDOTS_VARIABLE_SMOKE_LABEL, UBIDOTS_VARIABLE_HUMIDITY_LABEL]#making VARIABLES global variable

'''
TempSensorAdaptor - Class to get system's temperature sensor readings, send mail and take action.

@var __instance: singleton TempSensorAdaptor class instance variable.
@var sensorData: instance of SensorData class.
@var ActuatorData: instance of ActuatorData class.
@var SenseHat: instance of SenseHat class.
@var sensorReading: The sensor readings value
@var curTemp: current temperature sensor value.
@var prevTemp: previous temperature sensor value.
@var curSmoke: current smoke sensor value.
@var prevSmoke: previous smoke sensor value.
@var curHumidity: current humidity sensor value.
@var prevHumidity: previous humidity sensor value.
@var isPrevSensorReadingsSet: boolean to check whether previous sensor readings value is set or not.
@var timeInterval: regular time intervals to sense and process temperature sensor value. 
@var DataUtil: instance of DataUtil class.
'''
class SensorAdaptor(threading.Thread):

    __instance = None
    sensorData = None 
    ActuatorData = None
    SenseHat = None
    sensorReading = None
    curTemp = 0
    prevTemp = 0
    curSmoke = 0
    prevSmoke = 0
    curHumidity = 0
    prevHumidity = 0
    isPrevSensorReadingsSet = False
    timeInterval = 0
    DataUtil = None
    
    '''
    Static access method for singleton implementation.
    
    @return: '__instance' - singleton TempSensorEmulator class instance.
    ''' 
    @staticmethod 
    def getInstance():
        
        if SensorAdaptor.__instance == None:
            SensorAdaptor()
        return SensorAdaptor.__instance
    
    '''
    TempSensorEmulator Constructor to initialize.
    '''
    def __init__(self):
       
        if SensorAdaptor.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.beginEmulator = False
            self.threadName = "SensorAdaptor"
            self.sensorData = SensorData.SensorData()
            self.sensorReading = [0, 0, 0]
            self.curTemp = 0
            self.prevTemp = 0
            self.curSmoke = 0
            self.prevSmoke = 0
            self.curHumidity = 0
            self.prevHumidity = 0
            self.tempDiff = 0
            self.isPrevSensorReadingsSet = False
            self.timeInterval = 3
            self.ActuatorData = ActuatorData.ActuatorData()
            self.ActuatorAdaptor = ActuatorAdaptor.ActuatorAdaptor()
            self.SenseHat = SenseHat()
            self.DataUtil = DataUtil.DataUtil()
#             self.MQTTpublisher = MqttPubClient.MqttPubClient()
            self.MQTTsubscriber = MqttSubClient.MqttSubClient()
            self.HTTPpublisher = HTTPCloudPublisher.HTTPCloudPublisher()
            threading.Thread.__init__(self)
            SensorAdaptor.__instance = self
    
    '''
    Function to begin the Sensor Adaptor.
    
    @param value: True to start the Sensor Adaptor else False.  
    '''
    def setSensorAdaptor(self, value):
       
        self.beginEmulator = value 
    
    '''
    Thread function
    '''
    def run(self):

        self.MQTTsubscriber.connect()#subsciber connect method callback mqttclientconnecter
        
        while True:
            if self.beginEmulator:
                self.curTemp = self.SenseHat.get_temperature()  #get temperature from SenseHat
                self.sensorReading[0] = self.curTemp
                self.curSmoke = round(uniform(5.0, 100.0), 2)  #get pressure from SenseHat
                self.sensorReading[1] = self.curSmoke
                self.curHumidity = self.SenseHat.get_humidity()  #get humidity from SenseHat
                self.sensorReading[2] = self.curHumidity
                #self.curTemp = random.uniform(float(self.lowVal), float(self.highVal))
                self.sensorData.addValue(self.sensorReading)
                
                if self.isPrevSensorReadingsSet == False:
                    self.prevTemp = self.curTemp
                    self.prevSmoke = self.curSmoke
                    self.prevHumidity = self.curHumidity
                    self.isPrevSensorReadingsSet = True
                else:
                    print("Sensor json data : " + self.DataUtil.toJsonFromSensorData(self.sensorData))
                    self.MQTTsubscriber.subscribe(UBIDOTS_VARIABLES)
                    #self.MQTTpublisher.publish(UBIDOTS_DEVICE_LABEL, self.DataUtil.toJsonFromSensorData(self.sensorData))
                    if self.HTTPpublisher.publish(UBIDOTS_DEVICE_LABEL, self.DataUtil.toJsonFromSensorData(self.sensorData)) == False:
                        return
                    #calling actuator adap to proccess message to display in sensehat and through mail
                    self.ActuatorAdaptor.processMessage(self.MQTTsubscriber.connector.dataUtil.key, self.MQTTsubscriber.connector.dataUtil.ActuatorData)     
            sleep(self.timeInterval)
            #At the end after actuator process is done disconnect method is called
        self.MQTTsubscriber.disconnect()