import mccLog
import mailHelper
import os
import configReader
import win32api

class executor(object):
    def __init__(self, commandDict, openDict):
        self.mccLog = mccLog.mccLog()
        self.mailHelper = mailHelper.mailHelper()
        self.commandDict = commandDict
        self.openDict = openDict

    def execute(self,exe):
        subject = exe['subject']
        self.mccLog.mccWriteLog(u'开始处理命令')
        print("execute: ", subject)
        #self.mailHelper.sendMail('pass','Slave')
        if subject in self.commandDict:
            self.mccLog.mccWriteLog('执行命令')
            try:
                command = self.commandDict[subject]
                os.system(command)
                self.mailHelper.sendMail('Success','Boss')
                self.mccLog.mccWriteLog(u'执行命令成功')
            except Exception as e:
                self.mccLog.mccError('执行命令失败' + str(e))
                self.mailHelper.sendMail('error','Boss',e)
        elif subject in self.openDict:
            self.mccLog.mccWriteLog(u'打开文件')
            try:
                openFile = self.openDict[subject]
                win32api.ShellExecute(0, 'open', openFile,',', ",", 1)
                self.mailHelper.sendMail('Success','Boss')
                self.mccLog.mccWriteLog(u'打开文件成功')
            except Exception as e:
                self.mccLog.mccWriteLog(u'打开文件失败' + str(e))
                self.mailHelper.sendMail('error','Boss',e)
        else:
            self.mailHelper.sendMail('error','Boss','no such command')
