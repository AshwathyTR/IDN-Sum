import sys
path = sys.argv[1]
import os
import codecs
tot = 0
count = 0
import json
for file in os.listdir(path):
    #print(file)
    if 'json' in file and 'gz' not in file:
        with codecs.open(os.path.join(path, file), 'r', encoding = 'utf=8', errors = 'ignore') as f:
            data = json.load(f)
    else:
        continue
    count = count + len(data)
    #print(count)
    for entry in data:
        tot_tokens = 0
        for line in entry['src']:
            tot_tokens = tot_tokens + len(line)
        if len(entry['src'])==0:
            continue
        tot = tot + (tot_tokens/len(entry['src']))
        #print(tot)
avg = tot/count
print(avg)
