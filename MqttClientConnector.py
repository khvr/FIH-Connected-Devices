'''
Created on Mar 2, 2019

@author: hkalyan
'''

import logging 
import paho.mqtt.client as mqttClient  # MQTT client
import ssl 
from project import ConfigUtil
from project import SensorData
from project import DataUtil

'''
 MqttClientConnector: python class for implementing MQTT protocol connector
 This class has methods defined for both MQTT Publisher and subscriber
 
 @var port: MQTT port number in integer
 @var brokerAddr: complete address of the host server in String
 @var brockerKeepAlive: to stay active in integer
 @var mqttClient: instance of MQTT client class
 @var config: instance of ConfigUtil class
 @var dataUtil: instance of DataUtil class
'''
class MqttClientConnector(object):
 
    port = None
    brokerAddr = ""
    brockerKeepAlive = None
    mqttClient = None
    config = None
    dataUtil = None

    '''
    MqttClientConnector Constructor
    '''
    def __init__(self):
        
        self.createLogger()  # log the console output 
        self.mqttClient = mqttClient.Client()
        self.config = ConfigUtil.ConfigUtil()
        self.config.loadConfig()
        self.brokerAddr = self.config.getProperty(self.config.configConst.MQTT_CLOUD_SECTION, self.config.configConst.CLOUD_MQTT_BROKER)
        self.port = int(self.config.getProperty(self.config.configConst.MQTT_CLOUD_SECTION, self.config.configConst.SECURE_PORT_KEY))
        self.brockerKeepAlive = int(self.config.getProperty(self.config.configConst.MQTT_CLOUD_SECTION, self.config.configConst.KEEP_ALIVE_KEY))
        self.dataUtil = DataUtil.DataUtil()
        self.sensoData = SensorData.SensorData()
        self.username = self.config.getProperty(self.config.configConst.MQTT_CLOUD_SECTION, self.config.configConst.USER_NAME_TOKEN_KEY)
        self.password = ""
        self.TLS_CERT_PATH = r"ubidots_cert.pem"
        
    '''
    Function to create logger and console handler
    '''       
    def createLogger(self):
        
        # create logger
        self.logger = logging.getLogger('MQTTClientConnector')
        self.logger.setLevel(logging.DEBUG)
        
        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        
        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # add formatter to ch
        ch.setFormatter(formatter)
        
        # add ch to logger
        self.logger.addHandler(ch)
    
    '''
    Function to connect to the MQTT host server
    
    @param connectionCallback: connection call back function
    @param msgCallback: message call back function
    '''
    def connect(self, connectionCallback=None , msgCallback=None):
        
        if(connectionCallback != None):
            self.mqttClient.on_connect = connectionCallback
        else:
            self.mqttClient.on_connect = self.onConnect
            
        if(msgCallback != None) :
            self.mqclient.on_disconnect = msgCallback
        else :
            self.mqttClient.on_disconnect = self.onMessage
            
        self.mqttClient.on_message = self.onMessage    
        
        self.mqttClient.loop_start()
        self.mqttClient.username_pw_set(self.username, password=self.password)
        self.logger.info("Connecting to broker " + self.brokerAddr)
        self.mqttClient.tls_set(ca_certs=self.TLS_CERT_PATH, certfile=None,
                            keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
                            tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
        self.mqttClient.tls_insecure_set(False)
        self.mqttClient.connect(self.brokerAddr, self.port, self.brockerKeepAlive)
    
    '''
    Function to disconnect from the MQTT host server
    '''  
    def disconnect(self):
        
        self.mqttClient.loop_stop()
        self.logger.info("Disconneting the MQTT  broker connection ")
        self.mqttClient.disconnect()
    
    '''
    Function called when the broker responds to our connection request.
    
    @param flags: flags is a dict that contains response flags from the broker:
    flags['session present'] - this flag is useful for clients that are
        using clean session set to 0 only. If a client with clean
        session=0, that reconnects to a broker that it has previously
        connected to, this flag indicates whether the broker still has the
        session information for the client. If 1, the session still exists.
    @param rc: The value of rc determines success or not:
                0: Connection successful
                1: Connection refused - incorrect protocol version
                2: Connection refused - invalid client identifier
                3: Connection refused - server unavailable
                4: Connection refused - bad username or password
                5: Connection refused - not authorised
                6-255: Currently unused.
    '''   
    def onConnect(self , client , userData , flags , rc):
   
        print("On connect RC : " + rc)
        if rc == 0:
            self.logger.info("Connected OK returned Code: " + rc)
        else:
            self.logger.debug("Bad connection Returned Code: " + rc)
    
    '''
    Function called when a message has been received on a topic that the client subscribes to.
    When a message arrive this message prints the data and calls the updataActuatorData message
    from datautil class
    
    @param msg: MQTTMessage that describes all of the message parameters.
    '''
    def onMessage(self , msg):
        
        rcvdJSON = msg.payload.decode("utf-8")
        self.logger.info("\nReceived Topic is " + msg.topic + " --> \n" + str(rcvdJSON))
        self.dataUtil.updateActuatorData(msg.topic,rcvdJSON)
    
    '''
    Publish a message on a topic causing a message to be sent to the broker and subsequently from
    the broker to any clients subscribing to matching topics.

    @param topic: The topic that the message should be published on.
    @param msg: The actual message to send. If not given, or set to None a
    zero length message will be used. Passing an int or float will result
    in the payload being converted to a string representing that number. If
    you wish to send a true int/float, use struct.pack() to create the
    payload you require.
    @param qos: The quality of service level to use.
    '''
    def publishMessage(self , topic , msg , qos=2):
 
        if qos < 0 or qos > 2 :
            qos = 2
            
        #self.mqttClient.loop_start()
        self.logger.info("\nTopic : "+ str(topic) + "\nMessage :\n" + str(msg))
        self.mqttClient.publish(topic, msg, qos)
        #sleep(100)
        #self.mqttClient.loop_stop()
    
    '''
    Function to establish MQTT connection, publish and disconnect
    
    @param topic: topic of the MQTT message in string
    @param msg: message payload
    @param qos: The quality of service level to use
    '''
    def publishAndDisconnect(self , topic , msg, qos=2):
       
        self.logger.info("\nTopic :\n" + str(topic))
        self.connect()
        #while True :
        self.publishMessage(topic, msg, qos)
        self.disconnect()
    
    '''
    Function to subscribe the client to one or more topics
    
    @param topic: topic of the MQTT message in string
    @param connnectionCallback: call back function on subscribe/on message
    @param qos: The quality of service level to use
    '''
    def subscibetoTopic(self , topic , connnectionCallback=None , qos=2):
       
        
        self.logger.info('subscibetoTopic : ' + topic)
        if (connnectionCallback != None):
            self.mqttClient.on_subscribe(connnectionCallback)
            self.mqttClient.on_message(connnectionCallback)
        
        self.mqttClient.subscribe(topic , qos)

    '''
    Function to unsubscribe the client from one or more topics.
    
    @param topic: A single string, or list of strings that are the subscription topics to unsubscribe from.
    @param connnectionCallback: call back function on unsubscribe event
    '''  
    def unsubscibefromTopic(self , topic , connnectionCallback=None):
       
        if (connnectionCallback != None):
            self.mqttClient.on_unsubscribe(connnectionCallback)
               
        self.mqttClient.unsubscribe(topic)
    
    '''
    Function to establish MQTT connection, subscribe the client to one or more topics and disconnect
    
    @param topic: topic of the MQTT message in string
    @param connnectionCallback: call back function on unsubscribe event
    @param qos: The quality of service level to use
    '''
    def subscribeAndDisconnect(self , topic , connnectionCallback=None , qos=2):
        
        self.logger.info("\nTopic :\n" + str(topic))
        self.connect()
        self.subscibetoTopic(topic, connnectionCallback , qos)
        self.disconnect()