#!/usr/bin/python3
#coding=utf-8
#######################################################
#filename:autocrt.py
#author:syp
#date:2018-7-18
#function：自动巡检
#######################################################
import telnetlib
import time
from publicfunc import *
from global_list import *
from exceloper import *

class TelnetConnection(object):
    debuglevel = 1
    finish ='#'
    def __init__(self, host, port, username, password):
        self._host = host
        self._port = port
        self._username = username
        if(username =='root'):
            self.finish=b'#'
        else:
            self.finish = b'$'
        self._password = password
        self._transport = None
        self._sftp = None
        self._client = None
        self._connect()  # 建立连接
    def _connect(self):
        try:
            transport = telnetlib.Telnet(self._host, port=23, timeout=20)
        except Exception as e:
            print (e)
            return
        transport.set_debuglevel(self.debuglevel)
        # 输入登录用户名
        line = transport.read_until(b"login:",100)
        printlog(str(line) )
        transport.write(self._username.encode('ascii')+b'\n')
        printlog('input username:'+self._username)
        # 输入登录密码
        line =transport.read_until(b'assword:')
        printlog(str(line))
        transport.write(self._password.encode('ascii')+b'\n')
        printlog('input password:******')
        #line = transport.read_very_lazy()
        line = transport.read_until(self.finish,10)
        printlog(str(line))
        line = line.decode('utf-8')
        i = line.find('incorrect')
        if(i>=0):
            return
        if(line.find('Terminal type')>=0):
            transport.write(b'vt100\n')
            transport.read_until(self.finish, 2)
        self._transport = transport
        self.get_endsymbol()
        return
    def get_endsymbol(self):
        self._transport.write(b'\n')
        line = self._transport.read_until(self.finish, 2)
        line = line.decode('utf-8').strip().strip('\n')
        if line!='':
            self.finish = line[-1:].encode()
            return
        """
        if line.find('>')>=0:
            self.finish = b'>'
        if line.find('$') >= 0:
            self.finish = b'$'
        if line.find('#') >= 0:
            self.finish = b'#'
        return
        """

    def exec_command(self,cmd):
        self._transport.write(cmd.encode('ascii') + b'\n')
        #while True:
        #line = self._transport.read_until(b"\n",10)  # Check for new line and CR
         #   print(line.decode('utf-8'),end='')
         #print(self._transport.read_all().decode('ascii'))
        line = self._transport.read_until(self.finish, 10)  # Check for new line and CR
        return (line.decode('utf-8'))

    def get_hostname(self):
        self._transport.write('hostname'.encode('ascii') + b'\n')
        line = self._transport.read_until(self.finish,10)
        return  line.decode('utf-8').split('\r\n')[1]
    def get_df(self):
        self._transport.write('df -h'.encode('ascii') + b'\n')
        line = self._transport.read_until(self.finish,10)
        return (line.decode('utf-8'))

    def exec_command(self,cmd):
        self._transport.write(cmd.encode('ascii') + b'\n')
        line = self._transport.read_until(self.finish, 10)
        return (line.decode('utf-8'))

    def get_errmsg(self,devtype):
        if (devtype == 'linux'):
            cmd = 'tail -n 100 /var/log/messages|grep -E \"panic|error|warning\";tail -10 /var/log/warn | grep -E \"err|Err|warn|Warn|reset|Reset\"'
        elif (devtype == 'unix'):
            cmd = "tail -10 /var/adm/syslog/syslog.log | grep -E \"err|Err|warn|Warn|reset|Reset\""
        elif (devtype == 'AIX'):
            cmd = "tail -10 /var/adm/messages  | grep -E \"err|Err|warn|Warn|reset|Reset\""
        self._transport.write(cmd.encode('ascii') + b'\n')
        line = self._transport.read_until(self.finish, 10)
        return (line.decode('utf-8'))
    def close(self):
        self._transport.close()
def check_telnet_dev(device):
    sshconn = TelnetConnection(device['devip'],device['port'],device['devuser'],device['devpass'])
    dev_result=[]
    dev_result.append(device['devname'])
    dev_result.append(device['devip'])
    if (sshconn._transport == None):
        print ('connect failed')
        result_to_excel(dev_result, 0)
        return
    # 自定义命令
    #dev_result.append(get_errmsg(sshconn,device['devtype']))
    for cmd in range(titel_count,len(device)) :
        cmd = device['diycmd'+str(cmd-titel_count+1)]
        if(cmd.strip('')!=''):
            printlog(cmd)
            cmdresult = sshconn.exec_command (cmd)
            printlog(cmdresult)
            dev_result.append(cmdresult)
        else:
            dev_result.append('')
    result_to_excel(dev_result,0)
    sshconn.close()

if __name__ == '__main__':
    conn = TelnetConnection( "192.168.133.101", 23, 'sunyp', '123456')
    if (conn._transport == None):
        print ('connect failed')
    else:
        print ( conn.exec_command('ls'))
        print( conn.exec_command('df -k'))
        conn.close()
