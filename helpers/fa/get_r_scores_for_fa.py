from pyrouge import Rouge155
import sys
import pandas as pd
import os
path = sys.argv[1]
import shutil
df = pd.read_csv(path)
ref = sys.argv[2]
hyps = sys.argv[3:]
os.mkdir('hyp')
os.mkdir('ref')
for hyp in hyps:
    scores = []
    for index, row in df.iterrows():
        #print("hyp"+hyp)
        #print("ref"+ref)
        gen_sum = row[hyp]
        ref_sum = row[ref]
        #print(gen_sum)
        #print(ref_sum)
        r = Rouge155()
        r.system_dir = './hyp'
        r.model_dir = './ref'
        #r.system_filename_pattern = '0.txt'
        #r.model_filename_pattern = '0.txt'
        with open('./hyp/0.txt','w') as f:
            f.write(gen_sum)
        with open('./ref/0.txt','w') as f:
            f.write(ref_sum)
        r.system_filename_pattern = '(\d+).txt'
        r.model_filename_pattern = '#ID#.txt'

        command = '-e /home/atr1n17/pyrouge/tools/ROUGE-1.5.5/data -a -x -c 95 -m -n 1'
        output = r.convert_and_evaluate(rouge_args=command)

        output_dict = r.output_to_dict(output)
        score = output_dict["rouge_1_f_score"]
        scores.append(score)
    df = df.drop(hyp+'_r_scores',1)
    df.insert(1,hyp+'_r_scores',scores)
df.to_csv(path)
shutil.rmtree('./hyp')
shutil.rmtree('./ref')
