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
data_dir_mov = sys.argv[1]
import subprocess
import codecs
from gensim.summarization.textcleaner import clean_text_by_sentences
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
            for index, entry in enumerate(entries):
                data[fname+str(i+index)]['wiki_sum'] = entry
            
            i = len(data.keys())
              
    return data 

# load a spaCy model, depending on language, scale, etc.
#nlp = spacy.load("en_core_web_sm")
#nlp.add_pipe("textrank")

data_dir = sys.argv[1]
save_path = sys.argv[2]
sum_len = int(sys.argv[3])
data_s = extract_data(data_dir)
with open(os.path.join(save_path, 'hyp.txt'), 'w') as f:
        pass
with open(os.path.join(save_path, 'ref.txt'), 'w') as f:
        pass
 
from gensim.summarization import summarize
for movie in data_s.keys():
    #print('movie'+ str(movie))
    text = data_s[movie]['script']
    ref_sum = data_s[movie]['wiki_sum'] 
    #print(ref_sum[:100])
    sentences = clean_text_by_sentences(text)
    #required_ratio = float(sum_len)/float(len(sentences))
    if len(sentences)<sum_len:
        tr_sum = text
    else:
        required_ratio = float(sum_len)/float(len(sentences))
        tr_sum = summarize(text, ratio = required_ratio)
        
    _sum_len = len(tr_sum.split('\n'))
    #assert _sum_len == sum_len
    with open(os.path.join(save_path, 'hyp.txt'), 'a') as f:
        f.write(tr_sum+'<<END>>')
    with open(os.path.join(save_path, 'ref.txt'), 'a') as f:
        f.write(ref_sum+'<<END>>')
    
