# -*- coding: utf-8 -*-
"""
Created on Sat Aug 28 20:16:58 2021

@author: atr1n17
"""

import os
import random
import codecs
import sys

path = sys.argv[1]
w_path = sys.argv[2]
mode = sys.argv[3]

for movie in os.listdir(path):
        if not os.path.isfile(path+'\\'+movie+ r'\formatted_script.txt'):
            continue

        with codecs.open(path+'\\'+movie+ r'\formatted_script.txt','r', encoding='utf-8') as f:
             script = f.read()
        with codecs.open(mode+'.source','a',encoding='utf-8') as f:
            f.write(script+'\n')

               
        with codecs.open(w_path,'r', encoding='utf-8') as f:
            summ = f.read()
            summ = summ.replace('\n',' ')
        
        with codecs.open(mode+'.target','a',encoding='utf-8') as f:
            f.write(summ+'\n')
        



        