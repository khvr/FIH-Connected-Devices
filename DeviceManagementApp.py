'''
Created on Apr 15, 2019

@author: hkalyan
'''

from project import SensorAdaptor

'''
The Device Management App which has an instance of SensorAdaptor and starts a 
thread
'''

Adaptor = None  # TempSensorAdaptor instance variable
Adaptor = SensorAdaptor.SensorAdaptor().getInstance()  # get singleton instance of TempSensorAdaptor
Adaptor.daemon = True  # initiating the daemon
Adaptor.setSensorAdaptor(True)  # enabling the thread to begin TempSensorAdaptor
Adaptor.start()  # starting the TempSensorAdaptor thread

# infinite loop
while(True):
    pass