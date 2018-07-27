#!/usr/bin/python3
#coding=utf-8
#######################################################
#filename:
#author:syp
#date:2018-7-18
#function：自动巡检
#######################################################
import  sys
def printlog(logmsg):
    try:
        raise Exception
    except:
        f = sys.exc_info()[2].tb_frame.f_back
    print ("function:"+f.f_code.co_name+" "+str(f.f_lineno)+":"+logmsg)
    return
