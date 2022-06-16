# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 16:43:03 2021

@author: atr1n17
"""
import os
import sys

data_dir = sys.argv[1]

for fname in os.listdir(data_dir):
            if '.txt' in fname or '.pkl' in fname:
                continue
            script = os.path.join(data_dir, fname, "script.txt")
            with open(script,'r') as f:
                script_file = f.read()
            
            s1 = script_file.split("END OF EPISODE 1: AWAKE")
            #print(s1)
            script1 = s1[0]
            s2 = s1[1].split("END OF EPISODE 2: BRAVE NEW WORLD")
            script2 = s2[0]
            script3 = s2[1]
            with open(os.path.join(data_dir, fname, "script_1.txt"),'w') as f:
                f.write(script1)
            with open(os.path.join(data_dir, fname, "script_2.txt"),'w') as f:
                f.write(script2)
            with open(os.path.join(data_dir, fname, "script_3.txt"),'w') as f:
                f.write(script3)
            e2_choices = ["Don't screw up?\n", "Is that rhetorical?\n", "Say nothing.\n"]
            e3_choices = ["I'm here.\n", "You can handle this.\n"]            
            choices_file = os.path.join(data_dir, fname, "choices.txt")
            with open(choices_file, 'r') as f:
                choices = f.readlines()
            ep = 1
            ep_choices = {}
            ep_choices['1'] = []
            ep_choices['2'] = []
            ep_choices['3'] = []
            for choice in choices:
                #print(choice)
                if choice in e2_choices:
                    ep = 2
                    #print(choice)
                if choice in e3_choices:
                    ep = 3
                ep_choices[str(ep)].append(choice)
            for e in ep_choices.keys():
                with open(os.path.join(data_dir, fname, "choice_"+ str(e)+".txt"),'w') as f:
                    for choice in ep_choices[e]:
                        f.write(choice)
                        
                        
from shutil import copyfile
import os
eps = ['1','2','3']

for ep in eps:
    os.makedirs(data_dir+ep)
    for fname in os.listdir(data_dir):
        if '.txt' in fname or '.pkl' in fname:
            continue
        os.mkdir(os.path.join(data_dir+ep, fname))
        copyfile(os.path.join(data_dir, fname, 'choice_'+ep+'.txt'), os.path.join(data_dir+ep, fname, 'choices.txt'))
        copyfile(os.path.join(data_dir, fname, 'script_'+ep+'.txt'), os.path.join(data_dir+ep, fname, 'script.txt'))
    


