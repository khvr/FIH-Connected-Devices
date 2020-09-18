'''
Created on Apr 20, 2019

@author: khars
'''
from project import MqttClientConnector

UBIDOTS_DEVICE_LABEL = "rbcloud/"#Making this variable global
UBIDOTS_TOPIC_DEFAULT = "/v1.6/devices/"#Making this variable global
QOS = 2#Making this variable global

'''
SubClient creates an instance of MqttClientConnector and calls the functions required
for  subscibing a topic

@var connector: MqttClientConnector instance
'''
class MqttSubClient(object):
    
    connector = None
    
    '''
    MQTT subsciber constructor, initializes the MQTT client connector.
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
    subscribe method which calls MqttClientConnector  subscibetoTopic callback
    
    @param topic: The TOPIC_DEFAULT+DEVICE_LABEL+API-LABEL to subscribe to get data
    where topic is the API-LABEL
    ''' 
    def subscribe(self,topic):
        
        self.connector.subscibetoTopic(UBIDOTS_TOPIC_DEFAULT + UBIDOTS_DEVICE_LABEL + topic[0], None , QOS)
        self.connector.subscibetoTopic(UBIDOTS_TOPIC_DEFAULT + UBIDOTS_DEVICE_LABEL + topic[1], None , QOS)
        self.connector.subscibetoTopic(UBIDOTS_TOPIC_DEFAULT + UBIDOTS_DEVICE_LABEL + topic[2], None , QOS)