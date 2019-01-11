#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Gai Wang
import cx_Oracle as cxo
import os, math, re
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

class value_preprocess_2:
    def __init__(self, iter=100000,sql="select * from pingantest.RA_MER_BASE_QYNB_x40W27"):
        self.iter = iter
        self.sql=sql


    def parameter_transfer(self):
        connection_oracle = cxo.connect('system/pinganreader@10.3.70.71/orcl')
        cr = connection_oracle.cursor()
        result_sql = cr.execute(self.sql)
        result_fetch = result_sql.fetchall()
        new_result = []
        for line in result_fetch:
            line = self.truncate_line(self.trans(list(line)))
            new_result.append(line)
        return new_result

    def trans(self, line, *args):
        for j in range(len(line)):
            """index before truncate"""
            if j == 2 and line[2] == None:
                """currency"""
                line[2] = 156

            if j == 8 and line[8] != None:
                """ESTDATE"""
                line[8] = str(line[8]).split(' ')[0].split('-')[0]
                line[8] = self.year_huafen(line[8])

            if j == 14 and line[14] != None:
                """OPFROM"""
                line[14] = str(line[14]).split(' ')[0].split('-')[0]
                line[14] = self.year_huafen(line[14])

            if j == 15:
                """经营年长opyear"""
                line[15]=self.opyears(line[15])

            if j == 35 or j==20:
                """INVESTMONEY AND regcap"""
                line[j]=self.regcap_trans(line[j])

            if j in [26,27,36,57,63,71,73,79,81,84,85,86]:
                """BRANCH NUM,SUBENT NUM,LICENSE,SWJ_BAD_RECPRD,LOANCARD_COUNT,gjj_bad_count,SB_AB_YEARS,LIMIT_RECORD,HG_PUNCOUNT,CASE_COUNT,SWJ_PUNISH_RECORD,punish_sum"""
                """区域划分，只留下None 0 and 1"""
                line[j]=self.yes_or_no(line[j])

            if j == 57 and line[76] == 1 and line[57] == None:
                """税务异常"""
                line[57] = 0

            if j == 71 and line[77] == 1 and line[71] == None:
                """公积金异常"""
                line[71] = 0

            if j == 73 and line[j] == None:
                """社保欠缴，工商失信记录"""
                line[j] = 0

            if j == 72:
                line[72]=self.amonut_yes_or_no(line[72])

            if j==80 and line[79]>=1:
                line[80]=self.if_word(line[80])

            if j == 82 and line[81] >= 1:
                line[82]=self.if_word(line[82])

            if j ==87 :
                """criminal_times"""
                line[87]=self.criminal_times(line[87])
        return line

    def truncate_line(self, list_a):
        list_x = [0, 1, 3, 11, 12, 16, 17, 18, 19, 21, 22, 23, 24, 25, 28, 29, 30, 31, 32, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48,
                  49, 50, 51, 52, 53, 54, 55, 56, 58, 59, 60, 61, 62, 64, 65, 66, 67, 68, 69, 70,75]
        """去除掉不用于异常模型的字段"""
        for z in reversed(list_x):
            del list_a[z]
        return list_a

    def regcap_trans(self,number_a):
        if number_a==None:
            return 0
        if number_a<=100:
            return "small"
        if number_a<=500 and number_a>100:
            return "medium"
        if number_a>500:
            return "large"

    def opyears(self,intx):
        if intx==None:
            return None
        if type(intx)==int:
            if intx>=20:
                return "long time"
            if intx<20 and intx>=10:
                return "middle"
            if intx<10:
                return "short time"

    def year_huafen(self,int_a):
        if int (int_a) >= 2000 and int(int_a) < 2010:
            """estdate 划分为两个区间"""
            return "not larger than 10"
        if int (int_a) < 2000:
            return "before 2000"
        if int(int_a) >= 2008:
            return "after 2010"
        else:
            return "invalid"

    def amonut_yes_or_no(self,var):
        if type(var)==float and var>0:
            return "has amount"
        if var==None:
            return "has no record"

    def if_word(self,content):
        if content.read()==None:
            return "with_NO_chinese"
        if  re.search(u"[\u4e00-\u9fa5]+",content.read())!=None:
            return "WITH_Chinese"

    def yes_or_no(self,value):
        if type(value)==int:
            if value>=1:
                return 1
            if value<1:
                return 0
        if type(value)==str:
            value=int(value)
            if value>=1:
                return 1
            if value<1:
                return 0
        if type(value)==float:
            if value>=1.0:
                return 1
            if value<1.0:
                return 0
        if value==None:
            return 0

    def criminal_times(self,str_a):
        if str_a==None:
            return "no_violation"
        if int(str_a)==0:
            return "no_violation"
        if int (str_a)>0:
            return "has violation"


