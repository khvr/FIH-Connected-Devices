'''
Created on Apr 19, 2019

@author: hkalyan
'''

import time
import requests
from project import ConfigUtil

'''
This class publishes the passed payload to the cloud

@var url: The url passed to publish a payload
@var TOKEN: The Authentication token to make a handshake
'''

class HTTPCloudPublisher(object):

    url = ''
    TOKEN = ''
    
    '''
    Constructor of HTTPCloudPublisher
    '''
    def __init__(self):
       
        self.config = ConfigUtil.ConfigUtil()
        self.baseURL = self.config.getProperty(self.config.configConst.UBIDOTS_CLOUD_SECTION, self.config.configConst.CLOUD_BASE_URL)
        self.TOKEN = self.config.getProperty(self.config.configConst.MQTT_CLOUD_SECTION, self.config.configConst.USER_NAME_TOKEN_KEY)
    
    '''
    publish fuction which publishes a payload to a url
    
    @param label:the API label to which the fuction publishes
    @param payload: The json payload passed to publish to cloud 
    @return Ture if connection is established False if connection fails
    '''
    def publish(self, label, payload):
        # Creates the headers for the HTTP requests
        self.url = self.baseURL + label
        headers = {"X-Auth-Token": self.TOKEN, "Content-Type": "application/json"}
    
        # Makes the HTTP requests
        status = 400
        attempts = 0
        while status >= 400 and attempts <= 5:
            print("sending request: ")
            req = requests.post(url=self.url, headers=headers,data= payload )
            status = req.status_code
            print(req.status_code)
            attempts += 1
            time.sleep(1)
    
        # Processes results
        if status >= 400:
            print("[ERROR] Could not send data after 5 attempts, please check \
                your token credentials and internet connection")
            return False
    
        print("[INFO] request made properly, your device is updated")
        return True