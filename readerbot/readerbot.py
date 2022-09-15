# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 18:09:23 2021

@author: atr1n17
"""
import json
import re
    
def clean_script(s):
    entity_pattern = r'\[\[(.*?)\|(.*?)\]\]'
    while( re.search(entity_pattern,s) is not None):
        entity = re.search(entity_pattern,s)
        s = s.replace(entity.group(0),entity.group(2))
    speaker_pattern = r'\'\'\'(.*?):\'\'\''
    while( re.search(speaker_pattern,s) is not None):
        speaker = re.search(speaker_pattern,s)
        s = s.replace(speaker.group(0),'\n\n            '+speaker.group(1).upper()+'                \n')
    event_pattern = '\'\'(.*?)\'\''
    while( re.search(event_pattern,s) is not None):
        event = re.search(event_pattern,s)
        s = s.replace(event.group(0),event.group(1))
    while( re.search(r'<u>(.*?)</u>',s) is not None):
        u = re.search(r'<u>(.*?)</u>',s)
        s = s.replace(u.group(0),'')
    s = s.replace('<tabber>','')
    s = s.replace('</tabber>','')
    s = s.replace('<blockquote>','')
    s = s.replace('</blockquote>','')
    s = s.replace('}}', '')
    s = s.replace('{{','')
    s = s.replace('\'\'\'','')
    s = s.replace('\'\'','')
    #s = s.replace("(thinking)","")
    s = s.replace('[[','')
    s = s.replace(']]','')
    s = s.replace('|','')
    s = s.replace('<div align="center">','')
    s = s.replace('</div>','')
    s = s.replace('<br />', ' ')    
    trim = ''
    for line in s.split('\n\n'):
        trim = trim +'\n\n'+line if line.strip() != '' else trim    
    #end = trim.split('END OF EPISODE 3: HELL IS EMPTY')
    wscript=''
    for line in trim.split('\n'):
        #print(line)
        wscript = wscript +'\n'
        if ':SC:' not in line:
            wscript = wscript + '                 ' 
        wscript = wscript + line 
    return wscript

           
with open('set_triggers.json') as json_file:
    set_triggers = json.load(json_file)
with open('use_triggers.json') as json_file:
    use_triggers = json.load(json_file)
with open('backtalk_scores.json') as json_file:
    backtalk_scores = json.load(json_file)
with open('counters.json') as json_file:
    counters = json.load(json_file)
with open('bt_outcome_triggers.json') as json_file:
    bt_outcome_triggers = json.load(json_file)
with open('bt_triggers.json') as json_file:
    bt_triggers = json.load(json_file)
with open('scene_triggers.json') as json_file:
    scene_triggers = json.load(json_file)

    
def eval_bool(flags, condition):
    #print(condition)
    if type(condition) is str:
        if condition.startswith('!'):
            if condition in flags or condition[1:] not in flags:
                result = True
            else:
                result = False
        else:
            if condition in flags:
                result = True
            else:
                result = False
    else:
        if 'and' in condition.keys():
            result = True
            for clause in condition['and']:
                result = result and eval_bool(flags, clause)
        if 'or' in condition.keys():
            result = False
            for clause in condition['or']:
                result = result or eval_bool(flags, clause)
    return result
            

def is_valid(flags, choice):
    result = True
    if choice in use_triggers.keys():
        condition = use_triggers[choice]
        result =  eval_bool(flags, condition)  
    elif choice[1:] in use_triggers.keys():
        condition = use_triggers[choice[1:]]
        result =  eval_bool(flags, condition) 
    return result
   
                            

def calc_overlap(c1, c2):
    overlap = 0.0
    for c in c2:
        common = list(set(c1).intersection(c))
        overlap =  overlap + float(len(common))/float(len(list(set(c1))))    
    overlap = overlap/float(len(c2)) if len(c2) > 0 else 0.0
    return overlap

def get_min_choice(options, prev_choices, choices_covered):
    min_ =2.0
    choice = None
    for option in options:
        overlap = calc_overlap(prev_choices + [option], choices_covered)
        if overlap<min_:
            min_ = overlap
            choice = option
    return choice
        
def end_backtalk(prev_choice, state):
    if state['backtalk_score_neg'] + float(backtalk_scores[prev_choice]) < -0.9:
        state['is_backtalk'] = False
        state['backtalk_score_neg'] = 0.0
        state['backtalk_score_pos'] = 0.0
        state['flags'].append(state['bt_context']+'_lost')
        state['bt_context'] = None
        end = True
    elif state['backtalk_score_pos'] + float(backtalk_scores[prev_choice]) > 0.9:
        state['is_backtalk'] = False
        state['backtalk_score_neg'] = 0.0
        state['backtalk_score_pos'] = 0.0
        state['flags'].append(state['bt_context']+'_won')
        state['bt_context'] = None
        end = True
    else:
        end = False
    return end, state

def update_backtalk(prev_choice, state):
    if float(backtalk_scores[prev_choice]) >0.0:
        state['backtalk_score_pos'] = state['backtalk_score_pos'] + float(backtalk_scores[prev_choice])
    else:
        state['backtalk_score_neg'] = state['backtalk_score_neg'] + float(backtalk_scores[prev_choice])
    return state
  
def eval_counter_bool(count, condition):
    result = False
    if type(condition) is str:
        if condition.startswith('<'):
            result = count<int(condition.strip('<'))
        else:
            result= count>int(condition.strip('>'))
    else:
        if 'and' in condition.keys():
            result = True
            for clause in condition['and']:
                result = result and eval_counter_bool(count, clause)
        if 'or' in condition.keys():
            result = False
            for clause in condition['or']:
                result = result or eval_counter_bool(count, clause)
    return result
        
        
def get_flags(count, flag_thresholds):
    flags = []
    for flag in flag_thresholds.keys():
        if eval_counter_bool(count, flag_thresholds[flag]):
            flags.append(flag)
    return flags
    

                         
def get_maxvar_playthrough(content, state, prev_choices, preset_choices, choices_covered):      
    play = ''
    choices = []
    for counter in counters.keys():    
       if prev_choices[-1] in counters[counter]["triggers"].keys():
           state[counter] = state[counter] + float(counters[counter]["triggers"][prev_choices[-1]])               
           flags = get_flags(state[counter], counters[counter]['flag_thresholds'])
           for flag in counters[counter]['flag_thresholds'].keys():
               if flag in flags and flag not in state['flags']:
                   state['flags'].append(flag)
               elif flag not in flags and flag in state['flags']:
                   state['flags'].remove(flag) 
    if prev_choices[-1] in bt_triggers.keys():
                                state['bt_context'] = bt_triggers[prev_choices[-1]]
                                state['is_backtalk'] = True
                                state['backtalk_score_neg'] = 0.0
                                state['backtalk_score_pos'] = 0.0                   
    if prev_choices[-1] in set_triggers.keys():
                            for flag in set_triggers[prev_choices[-1]]:
                                #print(prev_choices[-1])
                                state['flags'].append(flag)
    for section in content:                               
                if type(section) is str:
                    if state['is_backtalk']:
                        if prev_choices[-1] in backtalk_scores.keys():
                            end, state = end_backtalk(prev_choices[-1], state)
                            if end:
                                   play = play+section if type(section) is str else play
                                   return play, choices, state
                            else:
                                state = update_backtalk(prev_choices[-1], state)                
                if type(section) is str:
                        play = play +section
                        bt_pattern = r'\[\[Backtalk#(.*?)\|(.*?)\]\]'
                        bt_match = re.search(bt_pattern, section)
                        if bt_match:                                
                                state['bt_context'] = bt_match.group(2)
                                state['is_backtalk'] = True
                                state['backtalk_score_neg'] = 0.0
                                state['backtalk_score_pos'] = 0.0                                             
                else:
                    options = list(section.keys())
                    choice = get_min_choice(options, prev_choices, choices_covered)
                    #index = options.index(choice)
                    count=0
                    skip = False
                    while not is_valid(state['flags'],choice):
                        if len(options) ==1 or count>(50000*len(options)):
                            skip= True
                            break
                        count=count+1
                        options.remove(choice)
                        choice = get_min_choice(options, prev_choices, choices_covered)
                        #index = options.index(choice)
                    if skip:
                        continue
                    if choice in backtalk_scores.keys() and not state['is_backtalk']:
                        continue
                    choices.append(choice)
                    playthrough, choices_taken, state = get_maxvar_playthrough(section[choice], state, choices, preset_choices, choices_covered)
                    play = play + '\n\n'+playthrough
                    choices = choices + choices_taken
    return play, choices, state

    

def get_maxvar_play(parsed_script, choices_covered, preset_choices=[]):   
    play = ''
    choices = ['START']
    state = {}
    state['is_backtalk'] = False
    state['backtalk_score_pos'] = 0.0
    state['backtalk_score_neg'] = 0.0
    state['flags'] = ['romance_low']
    for counter in counters.keys():
        state[counter] = 0.0
    for scene in parsed_script:
        #print(scene['name'])
        if "principal wells' office" in scene['name'].lower():
            counters['intimacy_score']['flag_thresholds']['romance_high'] = ">5"
            counters['intimacy_score']['flag_thresholds']['romance_low'] = "<6"
        if scene['name'] in scene_triggers.keys():
            if not eval_bool(state['flags'], scene_triggers[scene['name']]):
                continue
        play = play+':SC:'+'\n'
        playthrough, choices_taken, state = get_maxvar_playthrough(scene['content'], state, choices ,preset_choices, choices_covered)
        play = play + playthrough
        choices = choices + choices_taken
        #print(scene['name'])
    play = play+'\n:SC:'                    
    play = clean_script(play)
    return play, choices, state



