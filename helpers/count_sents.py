import os
import json
import sys
import codecs
sents = []
path = sys.argv[1]
for file in os.listdir(path):
    if 'json' in file and 'gz' not in file:
         with codecs.open(os.path.join(path,file),'r', encoding = 'utf-8', errors='ignore') as f:
               hh = json.load(f)
         for entry in hh:
               for line in entry['src']:
                   sents.append(''.join(line))
print(len(list(set(sents))))
