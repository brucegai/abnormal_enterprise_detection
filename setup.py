#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Gai Wang

from setuptools import setup

setup(name='abnormal_enterprise',version='0.1',description='to find out which enterprise is abnormal or not',
      packages=['enterprise_abnormal'],scripts=['main_function'],py_modules=['__init__','main_function','naive_bayes','SVM_model','test_model','value_preprocess'],
      install_requires=['scikit-learn>=0.19.1'],package_dir={'enterprise_abnormal':"enterprise_abnormal"},
      package_data={'enterprise_abnormal':['*.*','']})
