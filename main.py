#!/usr/bin/python3
#coding=utf-8
#######################################################
#filename:autocrt.py
#author:syp
#date:2018-7-18
#function：自动巡检
#######################################################

import os
from exceloper import *
from sshlogin import check_ssh_dev
from telnetlogin import *
from global_list import *
import sys
import getopt

if __name__ == '__main__':
    devlist=[]
    colcount = get_device_list(devlist,0)

    #自定义命令
    for i in range(titel_count,colcount):
        titellist.append("diycmd"+str(i-titel_count+1))
    #遍历设备列表
    create_dev_excel()
    for device in devlist:
        devdict = dict(zip(titellist,device))
        printlog("check device %10s:%12s...."%(devdict['devname'],devdict['devip']))
        if (devdict["logintype"] == "ssh2"):
            check_ssh_dev(devdict)
        elif (devdict["logintype"] == "telnet"):
            check_telnet_dev(devdict)
    print ("-"*40)
    input("press any key.....")

