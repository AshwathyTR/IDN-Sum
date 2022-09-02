import os
import json
import sys
import codecs
vocab = []
path = sys.argv[1]
for file in os.listdir(path):
    if 'json' in file and 'gz' not in file:
         with codecs.open(os.path.join(path,file),'r', encoding='utf-8',errors='ignore') as f:
               hh = json.load(f)
         for entry in hh:
               for line in entry['src']:
                    for word in line:
                         if word not in vocab:
                                vocab.append(word)
print(len(vocab))
