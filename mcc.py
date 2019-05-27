import time
import sys
import mailHelper
import configReader
import executor

__Author__ = 'me'
__Version__ = 1.0

class mcc(object):
    CONFIGPATH = '_config.ini'
    KEY_COMMAND = 'Command'
    KEY_OPEN = 'Open'
    KEY_BOSS = 'Boss'
    KEY_TIMELIMIT = 'timelimit'

    def __init__(self):
        self.exeList = []
        self.mailHelper = mailHelper.mailHelper()
        self.configReader = configReader.configReader(self.CONFIGPATH)
        commandDict = self.configReader.getDict(self.KEY_COMMAND)
        print("commands: ", commandDict)
        openDict = self.configReader.getDict(self.KEY_OPEN)
        print("open commands: ", openDict)
        self.timelimit = int(self.configReader.readConfig(self.KEY_BOSS, self.KEY_TIMELIMIT))
        print("timelimt: ", self.timelimit)
        self.executor = executor.executor(commandDict,openDict)
        self.toRun()

    def toRun(self):
        while True:
            self.run()
            time.sleep(self.timelimit)

    def run(self):
        self.mailHelper.loginMail()
        mailBody = self.mailHelper.acceptMail()
        if mailBody:
            exe = self.mailHelper.analysisMail(mailBody)
            print(self.exeList)
            if exe['date'] not in self.exeList:
                self.exeList.append(exe['date'])
            # if exe:
                # print(exe)
                self.executor.execute(exe)

if __name__ == '__main__':
    mcc = mcc()



