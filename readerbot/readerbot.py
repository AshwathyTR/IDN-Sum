# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 18:09:23 2021

@author: atr1n17
"""
import json
import re
from utils import remove_html_tags
    

           
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

BT_PATTERN = r'\[\[Backtalk#(.*?)\|(.*?)\]\]'

def eval_bool(flags, condition):
    """
    Evaluate a boolean expression based on the given flags and condition.
    Args:
            flags (list): A list of strings representing the flags set.
            condition (str or dict): A boolean expression in string or dictionary format.
    Returns:
            bool: True if the expression is True, False otherwise.
    """
    if type(condition) is str:
        
        if condition.startswith('!'):
            # Negated condition (e.g. "!a")
            if condition in flags or condition[1:] not in flags:
                result = True
            else:
                result = False
        else:
            # Normal condition (e.g. "a")
            if condition in flags:
                result = True
            else:
                result = False
    else:
        if 'and' in condition.keys():
            # Conjunction of conditions (e.g. {'and': ['a', '!b']})
            result = True
            for clause in condition['and']:
                result = result and eval_bool(flags, clause)
        if 'or' in condition.keys():
            # Disjunction of conditions (e.g. {'or': ['a', '!b']})
            result = False
            for clause in condition['or']:
                result = result or eval_bool(flags, clause)
    return result
            

def is_valid(flags, choice):
    """Check whether the given choice is valid based on the available flags and triggers.

    Args:
        flags (list): A list of strings representing the flags set.
        choice (str): The user's input choice.

    Returns:
        bool: True if the choice is valid, False otherwise.
    """

    result = True
    # Check if the choice is a valid trigger with a corresponding condition
    if choice in use_triggers.keys():
        condition = use_triggers[choice]
        result =  eval_bool(flags, condition)  
    # Check if the choice is a negated trigger with a corresponding condition
    elif choice[1:] in use_triggers.keys():
        condition = use_triggers[choice[1:]]
        result =  eval_bool(flags, condition) 
    return result
   
                            

def calc_overlap(c1, c2):
    """
    Calculate the overlap between two sets of items.

    Args:
        c1 (list): The first set of items.
        c2 (list): The second set of items.

    Returns:
        float: The overlap between the two sets, as a float between 0.0 and 1.0.
    """
    overlap = 0.0
    for c in c2:
        common = list(set(c1).intersection(c))
        overlap =  overlap + float(len(common))/float(len(list(set(c1))))    
    overlap = overlap/float(len(c2)) if len(c2) > 0 else 0.0
    return overlap

def get_min_choice(options, prev_choices, choices_covered):
    """
    Get the option with the minimum overlap with the previous choices and the covered choices.

    Args:
        options (list): A list of options to choose from.
        prev_choices (list): A list of previous choices.
        choices_covered (list): A list of choices that have already been covered.

    Returns:
        The option with the minimum overlap with the previous choices and the covered choices.
    """
    min_ =2.0
    choice = None
    for option in options:
        overlap = calc_overlap(prev_choices + [option], choices_covered)
        if overlap<min_:
            min_ = overlap
            choice = option
    return choice
        
def end_backtalk(choice, state):
    """
    Check if the backtalk has ended based on the choice and the current state.

    Args:
        choice (str): The previous choice made in the backtalk.
        state (dict): The current state dict.

    Returns:
        A tuple containing a boolean indicating whether the backtalk has ended and the updated state.

    """
    # Check if the backtalk has ended due to negative backtalk score
    if state['backtalk_score_neg'] + float(backtalk_scores[choice]) < -0.9:
        state['is_backtalk'] = False
        state['backtalk_score_neg'] = 0.0
        state['backtalk_score_pos'] = 0.0
        state['flags'].append(state['bt_context']+'_lost')
        state['bt_context'] = None
        end = True
    # Check if the backtalk has ended due to positive backtalk score
    elif state['backtalk_score_pos'] + float(backtalk_scores[choice]) > 0.9:
        state['is_backtalk'] = False
        state['backtalk_score_neg'] = 0.0
        state['backtalk_score_pos'] = 0.0
        state['flags'].append(state['bt_context']+'_won')
        state['bt_context'] = None
        end = True
    else:
        end = False
    return end, state

def update_backtalk(choice, state):
    """
    Update the backtalk scores in the given state based on the choice.

    Args:
        choice (str): The previous choice made.
        state (dict): A dictionary containing the state.

    Returns:
        The updated state dictionary.
    """
    if float(backtalk_scores[choice]) >0.0:
        state['backtalk_score_pos'] = state['backtalk_score_pos'] + float(backtalk_scores[choice])
    else:
        state['backtalk_score_neg'] = state['backtalk_score_neg'] + float(backtalk_scores[choice])
    return state
  
def eval_counter_bool(count, condition):
    """
    Evaluates a boolean expression involving a counter.

    Args:
    count (int): the value of the counter to be evaluated.
    condition (str or dict): the condition to be evaluated. 
        If a string, it must start with '<' or '>', indicating whether 
        the counter should be less than or greater than the number that follows.
        If a dictionary, it must contain either an 'and' or 'or' key, 
        with a list of sub-conditions to be evaluated as the value.

    Returns:
    bool: True if the condition is satisfied, False otherwise.

    """
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
    """
    Given a numerical count and a dictionary of flag names and their corresponding
    threshold values, returns a list of flags whose thresholds have been crossed
    based on the given count.

    Args:
    - count (int): A numerical count.
    - flag_thresholds (dict): A dictionary containing flag names as keys and
    their corresponding threshold values as values.

    Returns:
    - flags (list): A list of flags whose thresholds have been crossed based on
    the given count.
    """

    flags = []
    for flag in flag_thresholds.keys():
        if eval_counter_bool(count, flag_thresholds[flag]):
            flags.append(flag)
    return flags
   
def init_backtalk(state, context):
    """
    Initializes the backtalk in the given `state` dictionary with the given `context`.

    Args:
    - state (dict): A dictionary representing the current state of the conversation.
    - context (str): A string representing the context of the backtalk.

    Returns:
    - A dictionary representing the updated `state` after initializing the backtalk.
    """
    state['bt_context'] = context
    state['is_backtalk'] = True
    state['backtalk_score_neg'] = 0.0
    state['backtalk_score_pos'] = 0.0 
    return state
                                          
    
def update_state(counters, choice, state):
    """
    Update the state dictionary based on the counters, previous choice, and triggers.

    Args:
    - counters (dict): A dictionary containing the counters and their properties.
    - choice (list): Last choice made
    - state (dict): A dictionary containing the current state .

    Returns:
    - state (dict): A dictionary containing the updated state.
    """
    
    # update the counters and flags based on the current choice
    for counter in counters.keys():
        if choice in counters[counter]["triggers"].keys():
            state[counter] = state[counter] + float(counters[counter]["triggers"][choice])              
            flags = get_flags(state[counter], counters[counter]['flag_thresholds'])
            for flag in counters[counter]['flag_thresholds'].keys():
                if flag in flags and flag not in state['flags']:
                    state['flags'].append(flag)
                elif flag not in flags and flag in state['flags']:
                    state['flags'].remove(flag) 
                    
    # initialize the backtalk state if the current choice triggers backtalk                 
    if choice in bt_triggers.keys():
        state = init_backtalk(state, bt_triggers[choice])
    
    # add flags to the state dictionary if the current choice triggers flag-setting                                             
    if choice in set_triggers.keys():
        for flag in set_triggers[choice]:
            state['flags'].append(flag)          
    return state
    
                         
def get_playthrough_from_node(content, state, prev_choices, choices_covered):      
    """
    Generates a playthrough string and updates the game state based on the given content and state.

    Args:
        content (list): A list of strings and/or dictionaries representing the content of a game node.
        state (dict): A dictionary containing the current state of the game.
        prev_choices (list): A list of strings representing the previous choices made in the game.
        choices_covered (set): A set of strings representing the choices already covered in the game.

    Returns:
        play (str): A string representing the playthrough generated by the function.
        choices (list): A list of strings representing the choices made in the game.
        state (dict): A dictionary containing the updated state of the game.
    """
    play = ''
    choices = []
    
    # update the game state based on the previous choice
    state = update_state(counters, prev_choices[-1], state)
        
    for section in content:                               
        if type(section) is str:
            # check if the game is currently in backtalk mode and the previous choice is a valid one
            if state['is_backtalk'] and prev_choices[-1] in backtalk_scores.keys():
                end, state = end_backtalk(prev_choices[-1], state)
                if end:
                    play = play+section if type(section) is str else play
                    break
                else:
                    state = update_backtalk(prev_choices[-1], state)                
       
            play = play +section            
            # check if the section contains a backtalk trigger and update the game state accordingly
            bt_match = re.search(BT_PATTERN, section)
            if bt_match:                                
                state = init_backtalk(state, bt_match.group(2))
                                                            
        else:
            options = list(section.keys()) # get the list of choices available to the player
            choice = get_min_choice(options, prev_choices, choices_covered)  # get the minimum choice not covered yet
            count=0
            skip = False
            
            # loop until a valid choice is found or all options are exhausted
            while not is_valid(state['flags'],choice):
                if len(options) ==1 or count>(50000*len(options)):
                    skip= True
                    break
                count=count+1
                options.remove(choice)
                choice = get_min_choice(options, prev_choices, choices_covered)
                
            #skip if there is only one option or no valid options
            if skip:
                continue 
            
            #skip all backtalk options after exiting backtalk mode
            if choice in backtalk_scores.keys() and not state['is_backtalk']:
                continue
            
            choices.append(choice)
            
            # recursively call the function to generate the playthrough for the chosen option
            playthrough, choices_taken, state = get_playthrough_from_node(section[choice], state, choices, preset_choices, choices_covered)
            
            play = play + '\n\n'+playthrough
            choices = choices + choices_taken
    return play, choices, state

    

def get_script_playthrough(parsed_script, choices_covered):   
    """
    Generate a playthrough of the given script by simulating player's choices.

    Args:
    - parsed_script (dict): a parsed script as a dictionary with scene information.
    - choices_covered (list): a list of choices that have already been covered in previous playthroughs.
    
    Returns:
    - play (str): the full playthrough as a string, including player choices.
    - choices (list): a list of all choices made in the playthrough
    - state (dict): the final state of all counters and flags in the playthrough.
    """
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
        
        # Update flag thresholds for intimacy score at the starting of Scene 1 in Episode 2
        if "principal wells' office" in scene['name'].lower():
            counters['intimacy_score']['flag_thresholds']['romance_high'] = ">5"
            counters['intimacy_score']['flag_thresholds']['romance_low'] = "<6"
        
        if scene['name'] in scene_triggers.keys():
            if not eval_bool(state['flags'], scene_triggers[scene['name']]):
                continue
            
        play = play+':SC:'+'\n'
        playthrough, choices_taken, state = get_playthrough_from_node(scene['content'], state, choices, choices_covered)
        play = play + playthrough
        choices = choices + choices_taken
    play = play+'\n:SC:'                    
    play = remove_html_tags(play)
    return play, choices, state



