#!/usr/bin/python3
#coding=utf-8
#######################################################
#filename:getdevice.py
#author:syp
#date:2018-7-18
#function：获取excel 设备信息,返回list
#######################################################

import xlrd
import xlwt
from global_list import *
import xlutils.copy
import time

from publicfunc import *
def get_device_list( devlist,sheetnum ):
    "修改传入的列表"
    try:
        workbook = xlrd.open_workbook(devicefile)
    except Exception as e:
        print("can not open file "+devicefile)
        return 0
    #设备列表
    worksheetdev = workbook.sheets()[sheetnum]
    num_rows = worksheetdev.nrows
    num_cols = worksheetdev.ncols
    for curr_row in range(1,num_rows):
        rowval= worksheetdev.row_values(curr_row)
        listrow=[]
        for cols in range(len(rowval)):
            if(worksheetdev.cell(curr_row,cols).ctype == 2): #数字去小数点
                cellval= str(int(rowval[cols]))
                listrow.append(cellval)
            else:
                listrow.append(rowval[cols])
        devlist.append(listrow)
    return num_cols
def create_dev_excel():
    global resultfile
    resultfile += time.strftime("%Y%m%d%H%M%S", time.localtime())+'.xls'
    workbook = xlwt.Workbook(encoding = 'ascii')
    sheet1 = workbook.add_sheet('device', cell_overwrite_ok=True)
    # 初始化样式
    font = xlwt.Font()  # Create the Font
    font.name = '宋体'
    font.bold = True
    font.underline = False
    font.height = 0x00FF  #字体大小
    font.colour_index = 0
    #对齐
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    alignment.wrap = xlwt.Alignment.WRAP_AT_RIGHT

    #边框
    borders = xlwt.Borders()
    borders.left = borders.right = borders.top = borders.bottom = xlwt.Borders.THIN
    borders.left_colour= borders.right_colour = borders.top_colour = borders.bottom_colour = 0x40
    #底纹
    pattern = xlwt.Pattern()  # Create the Pattern
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN  # May be: NO_PATTERN,SOLID_PATTERN, or 0x00 through 0x12
    pattern.pattern_fore_colour =43
    #样式
    style = xlwt.XFStyle()  # Create the Style
    style.font = font  # Apply the Font to the Style
    style.alignment = alignment
    style.borders = borders
    style.pattern =pattern
    # 向sheet页中写入数据
    row = 0
    diylen = len(titellist) - titel_count
    #表头
    sheet1.write_merge(row, row, 0, 1+diylen, '设备巡检',style)
    row +=1
    sheet1.write(row, 0,  '设备名称',style)
    sheet1.write(row, 1, 'IP地址',style)
    #列宽
    sheet1.col(0).width = 4000 # 3333 = 1" (one inch).
    sheet1.col(1).width = 5555

    for i in range(2,diylen+2):
        sheet1.write(row, i, '命令', style)
        sheet1.col(i).width = 3333 * 6

    # 保存该excel文件,有同名文件时直接覆盖
    try:

        workbook.save(resultfile)
    except Exception as e:
        print (e)
#结果保存到excel
def result_to_excel(resultlist,sheetnum):
    # 打开一个workbook
    rb = xlrd.open_workbook(resultfile,formatting_info=True)
    wb = xlutils.copy.copy(rb)
    # 获取sheet对象，通过sheet_by_index()获取的sheet对象没有write()方法
    ws = rb.sheets()[sheetnum]
    worksheet = wb.get_sheet(sheetnum)
    num_rows = ws.nrows

    # 初始化样式
    font = xlwt.Font()  # Create the Font
    font.name = '宋体'
    font.height = 0x00FF  #字体大小
    font.colour_index = 0
    #对齐
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_LEFT
    alignment.wrap = xlwt.Alignment.WRAP_AT_RIGHT #自动换行
    #边框
    borders = xlwt.Borders()
    borders.left =  borders.right = borders.top = borders.bottom = xlwt.Borders.THIN
    borders.left_colour = borders.right_colour = borders.top_colour = borders.bottom_colour = 0x40
    #底纹
    pattern = xlwt.Pattern()  # Create the Pattern
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN  # May be: NO_PATTERN,SOLID_PATTERN, or 0x00 through 0x12
    pattern.pattern_fore_colour =43
    #样式
    style = xlwt.XFStyle()  # Create the Style
    style.font = font  # Apply the Font to the Style
    style.alignment = alignment
    style.borders = borders
    #style.pattern =pattern
    # 写入数据
    for cols in range(len(resultlist)):
        worksheet.write(num_rows, cols, resultlist[cols],style)
    wb.save(resultfile)

if __name__ == '__main__':
    create_dev_excel()
    list =[12,1213,'w34\n2\n3n4\n2',1231231,'werwer']
    result_to_excel(list,0)

