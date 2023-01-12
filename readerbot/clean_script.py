# -*- coding: utf-8 -*-
"""
Created on Sat Aug 28 17:08:56 2021

@author: atr1n17
"""
import sys
filter_lines = ['Navlinksnext=','pt-br:Episódio 1: Awake - Roteiro','ru: Эпизод 1: Пробуждение/Сценарий','Category:','ru:Эпизод 2: О дивный новый мир/Сценарий']
def clean_script(script):
    new_script = ""
    prev_line= ''
    for line in script.split('\n'):
        skip = False
        for fl in filter_lines:
            if fl in line:
                skip = True
        if skip:
            continue
        if line.strip():
            if prev_line.isupper() and prev_line.strip():
                new_script = new_script + ' : '+ line.strip()+' [EX] '
            else:
                if not line.isupper():
                    new_script = new_script + ' S0 : '+ line.strip()+' [EX] '
                else:
                    new_script = new_script + ' '+ line.strip()
        prev_line = line
    return new_script


import codecs
path = sys.argv[1]
num = sys.argv[2]
for n in range(0, num):
    script_file = path + str(n)+'\\script.txt'
    with codecs.open(script_file,'r', encoding= 'utf-8') as f:
        script = f.read()
    ns = clean_script(script)
    with codecs.open(path + str(n)+'\\formatted_script.txt','w', encoding='utf-8') as f:
        f.write(ns)


            
    
    