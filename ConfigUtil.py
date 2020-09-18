'''
Created on Jan 25, 2019

@author: hkalyan
'''

import configparser
import os
from project import ConfigConst

'''
ConfigUtil - Utility class to load and get configuration properties.

@var configConst:  ConfigConst instance.
@var isLoaded: boolean to check whether configuration file is loaded or not.
@var configFilePath: path of configuration file.
@var configData: configparser instance.
'''
class ConfigUtil(object):

    configConst = None
    isLoaded = False
    configFilePath = None
    configData = None

    '''
    ConfigUtil Constructor to initialize.
    '''
    def __init__(self):
        
        if (self.configData == None):
            self.configData = configparser.ConfigParser()
        if (self.configConst == None):
            self.configConst = ConfigConst.ConfigConst()
        self.configFilePath = self.configConst.DEFAULT_CONFIG_FILE_NAME
    
    '''
    checks whether configuration file is loaded.
    
    @return: 'isLoaded' - True, if configuration file is loaded else False. 
    '''
    def isConfigDataLoaded(self):
        
        return self.isLoaded
    
    '''
    reads the properties from configuration file and sets 'isLoaded' member variable.
    '''
    def loadConfig(self):
        
        if (os.path.exists(self.configFilePath)):
            self.configData.read(self.configFilePath)
            self.isLoaded = True
    
    '''
    returns the configuration file path.
    
    @return: 'configFilePath' - path of the configuration file.
    '''
    def getConfigFile(self):
        
        return self.configFilePath

    '''
    loads the configuration properties data and return's it.
    
    @param forceReload: False, to forcefully reload the configuration file else True.
    @return: 'configData' - configuration file data.
    '''
    def getConfigData(self, forceReload = False):
    
        if (self.isLoaded == False or forceReload):
            self.loadConfig()
            
        return self.configData

    
    '''
    returns the individual property's value under the given section.
    
    @param section: name of the section in configuration file.
    @param key: name of the key under the section whose value is needed.
    @return: value of a given property.
    '''
    def getProperty(self, section, key, forceReload = False):
        
        return self.getConfigData(forceReload).get(section, key)  