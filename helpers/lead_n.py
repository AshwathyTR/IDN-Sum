# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 11:58:35 2021

@author: atr1n17
"""


# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 11:39:15 2021

@author: atr1n17
"""





import os
import sys

#code_dir = r"/home/atr1n17/TransformerSum/TransformerSum/"

    

import subprocess
import codecs

def extract_data(rootdir_j):
    data={}
    i = 0
    for fname in ['test']:
        
            script_file = os.path.join(rootdir_j, fname+ ".source")
            entry={}
            

            wiki_file = os.path.join(rootdir_j, fname+ ".target")
            
            
            with codecs.open(script_file,encoding='utf-8') as f:
                entries = f.readlines()
            for index, entry in enumerate(entries):
                data[fname+str(i+ index)] = {}
                data[fname+str(i+ index)]['script'] = entry
            
            with codecs.open(wiki_file,encoding='utf-8') as f:
                entries = f.readlines()
            #print(len(entries))
            for index,entry in enumerate(entries):
                data[fname+str(i+ index)]['wiki_sum'] = entry
            
            i = len(data.keys())
              
    return data 

# load a spaCy model, depending on language, scale, etc.
#nlp = spacy.load("en_core_web_sm")
#nlp.add_pipe("textrank")

data_dir = sys.argv[1]
save_dir = sys.argv[2]
import os
if not os.path.exists(save_dir):
    os.makedirs(save_dir, exist_ok=True)
data_s = extract_data(data_dir)
with codecs.open(os.path.join(save_dir, 'hyp.txt'), 'w',encoding='utf-8') as f:
        pass
with codecs.open(os.path.join(save_dir, 'ref.txt'), 'w',encoding='utf-8') as f:
        #print(movie)
        pass


for index,movie in enumerate(data_s.keys()):
    #print('movie'+ str(movie))
    text = data_s[movie]['script']
    #tr_sum = text_rank(text)
    l_sum = '\n'.join(text.split('. ')[:int(sys.argv[3])])
    with codecs.open(os.path.join(save_dir, 'hyp.txt'), 'a',encoding='utf-8') as f:
        f.write(l_sum+'<<END>>')
    with codecs.open(os.path.join(save_dir, 'ref.txt'), 'a',encoding='utf-8') as f:
        #print(movie)
        f.write(data_s[movie]['wiki_sum']+'<<END>>')

