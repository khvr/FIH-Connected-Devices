'''
Created on Apr 20, 2019

@author: hkalyan
'''
from project import MqttClientConnector


UBIDOTS_TOPIC_DEFAULT = "/v1.6/devices/"#Making this variable global
QOS = 2#Making this variable global

'''
PubClient creates an instance of MqttClientConnector and calls the functions required
for publishing a message

@var connector: MqttClientConnector instance
'''
class MqttPubClient(object):
    
    connector = None
    '''
    MQTT publisher constructor, initializes the MQTT client connector.
    '''
    def __init__(self):
        
        self.connector = MqttClientConnector.MqttClientConnector()  # MQTT connector instance
    
    '''
    connect method which calls MqttClientConnector connect callback
    '''
    def connect(self):
        
        self.connector.connect()
    
    '''
    disconnect method which calls MqttClientConnector disconnect callback
    '''
    def disconnect(self):
        
        self.connector.disconnect()
    '''
    publish method which calls MqttClientConnector  publishMessage callback
    
    @param label: The device topic+label to which the data is passed to
    @param sJSONobj: The sensordata json passed to publish to cloud
    '''   
    def publish(self,label,sJSONobj):
        
        self.connector.publishMessage(UBIDOTS_TOPIC_DEFAULT + label, sJSONobj, QOS)