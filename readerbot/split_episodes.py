# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 17:36:21 2021

@author: atr1n17
"""

import os
import codecs

data_dir = r"C:\Users\atr1n17\Documents\experiments\wau_readerbot\Wolf_Among_Us_1250_"
delim =   "__FORCETOC__"
rem = ["Video Game Transcripts", "Category:Episodes", "Telltale Games' The Wolf Among Us."]
c_delim = "end ep"
for fname in os.listdir(data_dir):
            if '.txt' in fname or '.pkl' in fname:
                continue
            script = os.path.join(data_dir, fname, "script.txt")
            with codecs.open(script,'r', encoding='utf-8') as f:
                script_file = f.read()
            for r in rem:
                script = script.replace(r, '')
            s = script_file.split(delim)
            for n in range(1,6):
                with codecs.open(os.path.join(data_dir, fname, "script_"+str(n)+".txt"),'w', encoding='utf-8') as f:
                    f.write(s[n-1])
                    
                    
            choice_file = os.path.join(data_dir, fname, "choices.txt")
            with codecs.open(choice_file, 'r', encoding='utf-8') as f:
                choices = f.read()
                
            s = choices.split(c_delim)

            for n in range(1,6):
                with open(os.path.join(data_dir, fname, "choices_"+str(n)+".txt"),'w') as f:
                    f.write(s[n])
                        
                        
from shutil import copyfile
import os
data_dir = r"C:\Users\atr1n17\Documents\experiments\wau_readerbot\Wolf_Among_Us_1250_"
eps = ['1','2','3','4', '5']

for ep in eps:
    os.makedirs(data_dir+ep)
    for fname in os.listdir(data_dir):
        if '.txt' in fname or '.pkl' in fname:
            continue
        os.mkdir(os.path.join(data_dir+ep, fname))
        copyfile(os.path.join(data_dir, fname, 'choices_'+ep+'.txt'), os.path.join(data_dir+ep, fname, 'choices.txt'))
        copyfile(os.path.join(data_dir, fname, 'script_'+ep+'.txt'), os.path.join(data_dir+ep, fname, 'script.txt'))
    


