import sys
import os
paths = sys.argv[2:]
num = int(sys.argv[1])
hyps=[]
refs=[]
for path in paths:
    with open(os.path.join(path,'hyp.txt'),'r') as f:
        h = f.read().split('<<END>>')
    hyps.append(h)
    with open(os.path.join(path,'ref.txt'),'r') as f:
        h = f.read().split('<<END>>')
    refs.append(h)
    total = len(h) 
import random
sample_indices = random.sample(range(1, total), num)

output = {}
for hyp, ref, path in zip(hyps, refs, paths):
    output[path] = [hyp[i] for i in sample_indices]
    output[path+'_abs'] = [ref[i] for i in sample_indices]
    
    

import pandas as pd
df = pd.DataFrame(output)
df.to_csv('data_for_fa.csv') 
