from email.mime.text import MIMEText
import poplib
import re
import smtplib
import mccLog
import configReader

class mailHelper(object):
    CONFIGPATH = '_config.ini'

    def __init__(self):
        self.mccLog = mccLog.mccLog()
        cfReader = configReader.configReader(self.CONFIGPATH)
        self.pophost = cfReader.readConfig('Slave', 'pophost')
        self.smtphost = cfReader.readConfig('Slave', 'smtphost')
        self.port = cfReader.readConfig('Slave', 'port')
        self.username = cfReader.readConfig('Slave', 'username')
        self.password = cfReader.readConfig('Slave', 'password')
        self.bossMail = cfReader.readConfig('Boss','mail')
        self.loginMail()
        self.configSlaveMail()

    def loginMail(self):
        self.mccLog.mccWriteLog(u'开始登录邮箱')
        try:
            self.pp = poplib.POP3_SSL(self.pophost)
            self.pp.set_debuglevel(0)
            self.pp.user(self.username)
            self.pp.pass_(self.password)
            self.pp.list()
            print('登录成功')
            self.mccLog.mccWriteLog(u'登录邮箱成功')
        except Exception as e:
            print('登录失败')
            self.mccLog.mccWriteLog(u'登录邮箱失败' + str(e))
            exit()

    def acceptMail(self):
        self.mccLog.mccWriteLog(u'开始抓取邮件')
        try:
            ret = self.pp.list()
            mailbody = self.pp.retr(len(ret[1]))
            self.mccLog.mccWriteLog(u'抓取邮件成功')
            return mailbody
        except Exception as e:
            self.mccLog.mccWriteLog(u'抓取邮件失败' + str(e))
            return None

    def analysisMail(self, mailbody):
        self.mccLog.mccWriteLog(u'开始抓取subject和发件人')
        try:
            subject = re.search("'Subject: (.*?)'",str(mailbody[1]),re.S).group(1)
            sender = re.search("'X-Sender: (.*?)'",str(mailbody[1]),re.S).group(1)
            date = re.search("'Date: (.*?)'",str(mailbody[1]),re.S).group(1)
            print("subject: ", subject)
            print("sender: ", sender)
            print("date: ", date)
            command = {'date': date, 'subject': subject,'sender': sender}
            self.mccLog.mccWriteLog(u'抓取邮件和发送人成功')
            return command
        except Exception as e:
            self.mccLog.mccWriteLog(u'抓取邮件和发送人失败' + str(e))
            return None

    def configSlaveMail(self):
        self.mccLog.mccWriteLog(u'开始配置发件箱')
        try:
            self.handle = smtplib.SMTP(self.smtphost,self.port)
            self.handle.login(self.username,self.password)
            self.mccLog.mccWriteLog(u'发件箱配置成功')
        except Exception  as e:
            self.mccLog.mccWriteLog(u'发件箱配置失败' + str(e))
            exit()

    def sendMail(self, subject, receiver, body = 'success'):
        msg = MIMEText(body,'plain','utf-8')
        msg['Subject'] = subject
        msg['from'] = self.username
        self.mccLog.mccWriteLog(u'开始发送邮件' + 'to' + receiver)
        if receiver == 'Slave':
            try:
                self.handle.sendmail(self.username, self.username, msg.as_string())
                self.mccLog.mccWriteLog(u'发送邮件成功')
                return True
            except Exception as e:
                self.mccLog.mccWriteLog(u'发送邮件失败' + str(e))
                return False
        elif receiver == 'Boss':
            try:
                self.handle.sendmail(self.username, self.bossMail, msg.as_string())
                self.mccLog.mccWriteLog(u'发送邮件成功')
                return True
            except Exception as e:
                self.mccLog.mccWriteLog(u'发送邮件失败' + str(e))
                return False

# if __name__ == '__main__':
#     mail = mailHelper()
    #mailbody = mail.acceptMail()
    #print((mailbody[1][8]).decode())
    #command = mail.analysisMail(mailbody)
    #print(command)
    #command = mail.analysisMail(body)
    #print(body)
    #print(command)
    #mail.sendMail('test', 'Boss')
