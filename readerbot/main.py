# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 13:19:17 2021

@author: atr1n17
"""
import sys
import os
sys.path = [os.getcwd()] + sys.path
from parse_html import get_parsed_script
from readerbot import get_maxvar_play
import json

with open('bt_outcome_triggers.json') as json_file:
    bt_outcome_triggers = json.load(json_file)

def insert_context(script):
    index = {}
    for bt_outcome_trigger in bt_outcome_triggers.keys():
        index[bt_outcome_trigger] = 0
    s = ''
    for line in script.split('\n'):
        for bt_outcome_trigger in bt_outcome_triggers.keys():
            if  bt_outcome_trigger+'=' in line:
                try:
                    line = line.replace(bt_outcome_trigger, bt_outcome_triggers[bt_outcome_trigger][index[bt_outcome_trigger]])
                except:
                    pass
                index[bt_outcome_trigger] = index[bt_outcome_trigger] +1
        s = s + line +'\n'
    return s   


def get_script(lis_url, page_id, begin_pattern):
    r = requests.get(lis_url)
    response = r.json()
    #print(response['query']['pages'].keys())
    script = response['query']['pages'][str(page_id)]['revisions'][-1]['*']
    beg = re.search(begin_pattern, script)
    episode = beg.group(1)
    
    script = script[beg.end():]
    if "Bigby sees marks on the window." in script:
        script = script.replace("Bigby sees marks on the window.", "Bigby sees marks on the window..\n}}")

    incom_block = "{{#tag:tabber|(Went here last)=\n\n'''Jersey:''' How you feeling today, Sheriff?<br />\n\nJersey punches Bigby in the back of the head.<br />\n\n'''Jersey:''' Still looking for whoever killed them hookers or are you done chasing your tail?<br />\n\nWoody grabs Jersey's neck and slams his face into a display case.<br />\n\n'''Woody:''' Where's my axe! Who'd you give it to!"
    com_block = incom_block+'\n}}'
    if incom_block in script:
        script = script.replace(incom_block, com_block)
    script = script.replace('<span style="font-size:larger">\'\'\'','').replace('</span>','')
    rev_num = str(len(response['query']['pages'][str(page_id)]['revisions']) -1)
    return  rev_num, script
 
def get_request(wiki_name,page_name):
    url = "https://"+ wiki_name + ".fandom.com/api.php?action=query&prop=revisions&titles=" + page_name.replace(' ','%20').replace('&','%26').replace('\'','%27')+ "&rvprop=content&format=json"
    page_id = vars(wikia.page(wiki_name, page_name))['pageid']
    return url, page_id
     
import codecs
import requests
import re
import os
import wikia
import pickle

def write_files(path, sample, index):
        os.makedirs(path + str(index+1))
        with codecs.open(path +str(index+1)+'/script.txt','w', encoding = 'utf-8') as w:
            w.write(sample[0])
        with codecs.open(path +str(index+1)+'/choices.txt','w', encoding = 'utf-8') as w:
            for choice in sample[1]:
                w.write(choice + '\n')
        

def write_meta(path, data, script, parsed):
    with codecs.open(path+'meta_data.txt','w', encoding = 'utf-8') as w:
        w.write(str(data))
    with codecs.open(path+'raw_script.txt','w', encoding = 'utf-8') as w:
        w.write(str(script))
    with open(path +'parsed_script.pkl','wb') as w:
           pickle.dump(parsed, w)


def get_maxvar_plays(count, parsed_script, save_path):
    samples = []
    choices_covered = []
    for index in range(0,count,1):
        print(index)
        sample = get_maxvar_play(parsed_script, choices_covered)
        choices_covered.append(sample[1])
        write_files(save_path, sample, index)


def gen_lis(wiki_name, ep_names, num_playthroughs, save_path, begin_pattern):
    full_script=''
    for ep_name in ep_names:
        lis_url, page_id = get_request(wiki_name, ep_name)
        #print(lis_url)
        #print(page_id)
        rev, script = get_script(lis_url, page_id, begin_pattern)
        full_script = full_script+ "\n==EP END==\n" + script
    
    script = insert_context(full_script)
    full_parsed_script = get_parsed_script(script)
    get_maxvar_plays(num_playthroughs, full_parsed_script, save_path)
    write_meta(save_path, rev, full_script, full_parsed_script)
    
   



wau_begin_pattern = r'The following is a \'\'\'transcript\'\'\' of \[\[(.*?)\]\]'

gen_lis("fables",["Faith_(Episode)/Transcript", "Smoke_&_Mirrors/Transcript", "A_Crooked_Mile/Transcript","In_Sheep's_Clothing/Transcript", "Cry_Wolf/Transcript"] , 1250, 'Wolf_Among_Us_1250_/sample_', wau_begin_pattern)

