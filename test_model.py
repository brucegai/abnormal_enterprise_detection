#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Gai Wang
import cx_Oracle as cxo
import os,numpy,json,csv
from abnormal_enterprise import value_preprocess_2
from sklearn.externals import joblib
from sklearn.preprocessing import Imputer
from matplotlib import pyplot
from abnormal_enterprise import value_preprocess


os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

class test_function:
    """this test_model function is used after the model is built"""
    def __init__(self,fake_parameter="yes",company_ID="None",doc_dict="27_dict_1229.json",model_file="svm_27_1229.model"):
        self.fake_parameter=fake_parameter
        self.company_ID=company_ID
        self.doc_dict=doc_dict
        self.svm_model=model_file

    def test_function_one(self):
        """first import test data"""
        connection_oracle = cxo.connect('system/pinganreader@10.3.70.71/orcl')
        cr = connection_oracle.cursor()
        result_sql = cr.execute("select * from pingantest.ra_mer_base_qynb_test_all")
        result_fetch = result_sql.fetchall()
        new_result = []
        for line in result_fetch:
            line = value_preprocess.value_preprocess().truncate_line(value_preprocess.value_preprocess().trans(list(line)))
            new_result.append(line)
        return new_result

    def test_model_function_naive(self):
        data=self.test_function_one()
        data = numpy.array(data)
        file_a=open(self.doc_dict,'r',encoding='utf-8')
        json_a=json.load(file_a)
        target_data = data[:, -1]
        data = numpy.delete(data[:, :-1], 2, 1)
        for item in data:
            for j in range(33):
                try:
                    item[j]=json_a[0].get(str(item[j])+"_"+str(j))
                except Exception as e:
                    item[j]=0.0001
                    continue
        """test_model_function"""
        model_a=joblib.load('Bayes_one_27.model')
        data = Imputer().fit_transform(data)
        result = model_a.predict(data)
        w=0
        for i,j in zip(target_data,result):
            if i==int(j):
                w+=1
        print(w / 40000)

    def test_model_function_svm(self):
        data = self.test_function_one()
        data = numpy.array(data)
        file_a = open(self.doc_dict, 'r', encoding='utf-8')
        json_a = json.load(file_a)
        target_data = data[:, -1]
        name_list=data[:,2]

        data = numpy.delete(data[:, :-1], 2, 1)
        for item in data:
            for j in range(len(item)):
                try:
                    item[j] = json_a[0].get(str(item[j]) + "_" + str(j))
                except Exception as e:
                    item[j] = 0.0001
                    continue
        model_a = joblib.load(self.svm_model)
        data = Imputer().fit_transform(data)
        result = model_a.predict(data)
        w = 0
        error_list=[]
        for i, j ,name in zip(target_data, result,name_list):
            if i == int(j):
                w += 1
            if i==0 and j==1:
                w += 1
            if i==1 and j==0:
                error_list.append([name])
        with open('wrong_list.csv','w',newline='',encoding='utf-8')as file_w:
            csvwriter=csv.writer(file_w)
            for line in error_list:
                csvwriter.writerow(line)
        # print(w / 40000,error_list,len(error_list))

    def test_all(self):
        data = self.test_function_one()
        data = numpy.array(data)
        file_a = open('27_dict.json', 'r', encoding='utf-8')
        json_a = json.load(file_a)
        target_data = data[:, -1]
        data = numpy.delete(data[:, :-1], 2, 1)
        for item in data:
            for j in range(len(item)):
                try:
                    item[j] = json_a[0].get(str(item[j]) + "_" + str(j))
                except Exception as e:
                    item[j] = 0.0001
                    continue
        model_a = joblib.load('svm_27.model')
        data = Imputer().fit_transform(data)
        result = model_a.predict(data)
        w = 0
        for i, j in zip(target_data, result):
            if i == int(j):
                w += 1
            if i==0 and j==1:
                w += 1
        print(w / 40000)


    def single_enterprise_test(self,*args):
        sql="select * from pingantest.RA_MER_BASE_QYNB_PINGANTEST_x t where t.PRIPID ='"+self.company_ID+"'"
        """得到异常的标记， 1： 异常 0：非异常"""
        data_a=value_preprocess_2.value_preprocess_2(sql=sql).parameter_transfer()
        data_a=numpy.array(data_a)
        file_a = open(self.doc_dict, 'r', encoding='utf-8')
        json_a = json.load(file_a)
        """调试数据应当去除YCML的字段"""
        data_a = numpy.delete(data_a[:,:-1], 2, 1)
        print(data_a.shape)
        print(data_a)
        for j in range(len(data_a[0])):
            try:
                data_a[0][j] = json_a[0].get(str(data_a[0][j])+"_"+str(j))
            except Exception as e:
                print(e)
        print(data_a[0])
        model_a = joblib.load(self.svm_model)
        data = Imputer().fit_transform(data_a)
        result = model_a.predict(data)
        if result[0]==1:
            print(["异常"])
        if result[0]==0:
            print(["正常"])


