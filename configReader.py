import configparser
import os,sys

class configReader(object):
    def __init__(self, configPath):
        configFile = os.path.join(sys.path[0], configPath)
        self.cReader = configparser.ConfigParser()
        self.cReader.read(configFile)

    def readConfig(self,section,item):
        return self.cReader.get(section,item)

    def getDict(self, secction):
        commandDict = {}
        items = self.cReader.items(secction)
        for key, value in items:
            commandDict[key] = value
        return commandDict