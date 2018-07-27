#!/usr/bin/python3
#coding=utf-8
#######################################################
#filename:
#author:syp
#date:2018-7-18
#function：自动巡检
#######################################################
import paramiko
import sys
from publicfunc import *
from global_list import *
from exceloper import *

def getssh2Connect( host, port, username, password):
    for i in (0,3):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, int(port), username, password)
            # 创建会话
            channel = ssh.invoke_shell()
            channel.settimeout(100)
            return ssh
        except Exception as e:
            print( e)
            return 'error'

#获取主机名
def get_hostname(conn):
    cmd_hostname = "hostname"
    stdin, stdout, stderr = conn.exec_command(cmd_hostname)
    hostname = stdout.read().decode('utf-8')
    return hostname

#获取磁盘空间
def get_df(conn):
    cmd1 = "df -h"
    cmd2 =  "df -h|awk '{print $5}'|grep -Eo '[0-9]+'"
    threshold =1
    stdin1, stdout1, stderr1 = conn.exec_command(cmd1)
    stdin2, stdout2, stderr2 = conn.exec_command(cmd2)
    thresList=[]
    result = stdout1.read().decode('utf-8')
    resultlist = result.split('\n')
    #print(resultlist)
    result2 = stdout2.read().decode('utf-8')
    resultlist2 = result2.split('\n')
    #print (resultlist2)
    for i in range(0, len(resultlist2)-1):
        if int(resultlist2[i]) >= threshold:
            thresList.append (resultlist[i])
    #print (thresList)
    return thresList
#test
def get_diy(conn,cmd):
    stdin1, stdout, stderr = conn.exec_command(cmd)
    result = stdout.read().decode('utf-8')
    if(result.strip('')==''):
        result = stderr.read().decode('utf-8').strip('')

    return result
#R3单板硬盘状态
def get_R3status(conn):
    stdin1, stdout, stderr = conn.exec_command("disk_info_test|grep Status|awk '{print $5}'")
    result = stdout.read().decode('utf-8')
    if(result.strip('')==''):
        result = stderr.read().decode('utf-8').strip('')
    return result
#R3单板硬盘状态
def get_R3ONL(conn):
    stdin1, stdout, stderr = conn.exec_command("disk_info_test |grep ONL|awk '{print $3}'")
    result = stdout.read().decode('utf-8')
    if(result.strip('')==''):
        result = stderr.read().decode('utf-8').strip('')
    return result

#linux日志
def get_errmsg(conn,devtype):
    if(devtype == 'linux'):
        cmd = "tail -n 100 /var/log/messages|grep -E \"panic|error|warning\";tail -10 /var/log/warn | grep -E \"err|Err|warn|Warn|reset|Reset\""
    elif (devtype == 'unix'):
        cmd = "tail -10 /var/adm/syslog/syslog.log | grep -E \"err|Err|warn|Warn|reset|Reset\""
    elif(devtype =='AIX'):
        cmd = "tail -10 /var/adm/messages  | grep -E \"err|Err|warn|Warn|reset|Reset\""

    stdin1, stdout, stderr = conn.exec_command(cmd)
    error = stderr.read().decode('utf-8')
    result = stdout.read().decode('utf-8').strip('')
    if not error:
        return result
    else:
        return error

def exec_diycmd(conn,diycmd):
    stdin, stdout, stderr = conn.exec_command(diycmd)
    result = stdout.read().decode('utf-8')
    if(result.strip('')==''):
        result = stderr.read().decode('utf-8').strip('')
        if (result.strip('') == ''):
            result ='no output'
    return result
#基本巡检函数
def check_ssh_dev(device):
    sshconn = getssh2Connect(device['devip'],device['port'],device['devuser'],device['devpass'])
    dev_result=[]
    dev_result.append(device['devname'])
    dev_result.append(device['devip'])
    if (sshconn =='error'):
        dev_result.append('connect error')
        result_to_excel(dev_result, 0)
        return
    #自定义命令
    for cmd in range(titel_count,len(device)) :
        cmd = device['diycmd'+str(cmd-titel_count+1)]
        if(cmd.strip('')!=''):
            printlog(cmd)
            cmdresult= exec_diycmd (sshconn,cmd)
            printlog(cmdresult)
            dev_result.append(cmdresult)
        else:
            dev_result.append('')
    result_to_excel(dev_result,0)
    sshconn.close()

