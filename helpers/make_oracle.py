# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 00:52:51 2022

@author: atr1n17
"""

import codecs
import json
import os
import sys
path = sys.argv[1]
save_path = sys.argv[2]
counter = 0
if not os.path.exists(save_path):
    os.makedirs(save_path, exist_ok=True)
with codecs.open(os.path.join(save_path, 'hyp.txt'),'w',encoding='utf-8') as f:
    pass
with codecs.open(os.path.join(save_path, 'ref.txt'),'w',encoding='utf-8') as f:
    pass

file_nums = [int(f.split('test.')[1].split('.json')[0]) for f in os.listdir(path) if 'test' in f and 'json' in f]
file_nums.sort()
for file_num in file_nums:
    file = 'test.'+str(file_num)+'.json'
    with codecs.open(os.path.join(path, file), 'r', encoding = 'utf-8') as f:
        data = json.load(f)
    
    for index, entry in enumerate(data):
        indices = [i for i, x in enumerate(entry['labels']) if x == 1]
        summ = '\n'.join([' '.join(entry['src'][i]) for i in indices])
        with codecs.open(os.path.join(save_path, 'hyp.txt'),'a',encoding='utf-8') as f:
            f.write(summ+'<<END>>')
        with codecs.open(os.path.join(save_path, 'ref.txt'),'a',encoding='utf-8') as f:
            f.write('\n'.join(entry['tgt'].split('<q>'))+'<<END>>')
        counter = counter +1
