# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 19:34:51 2021

@author: atr1n17
"""


import json
import random 
import time
from rouge import Rouge
import re

def is_complete_section(block):

    openblocks = block.count('#tag:tabber')
    closedblocks = block.count('\n}}')

    return openblocks == closedblocks

def is_complete_block(block):
    openblocks = block.count('<blockquote')
    closedblocks = block.count('/blockquote>')
    return openblocks == closedblocks

def has_nests(block):
    return block.count('#tag:tabber')>0

def has_elses(block):
    return block.count('{{!}}-{{!}}')>0
    
def get_level_1_blocks(dev):
    '''

    Parameters
    ----------
    dev : string 
    a section of the script enclosed by <tabber> </tabber> representing non linear if-else structure where else-blocks are separated using ||-||

    Returns
    -------
    blocks : List of strings
    List of else-blocks at the top level (nests are not split up)

    '''
    
    rem = dev
    blocks = []
    alt = re.search(r'\|\-\|',rem)
    while(alt is not None):
        blocks.append(rem[:alt.start()])
        rem = rem[alt.end():]
        alt = re.search(r'\|\-\|',rem)
    blocks.append(rem)
    return blocks

def get_complete_section(block, nest_start): 
    '''
    Parameters
    ----------
    block : String
        HTML text containing nested {{<#tag:tabber> {{!}}-{{!}} }}
    nest_start : re search result object
        position of the start of the nest that we want to extract

    Returns
    -------
    nest : string
        Text up until the }} indicating closing of the nest that started at nest_start
    nest_index : int
        Index in block where the nest ends

    '''
    nest = ''
    nest = nest + block[nest_start.start():nest_start.end()]
    nest_index = nest_start.end()
    #print(block)
    while(not is_complete_section(nest)):
        nest = nest + block[nest_index]
        nest_index = nest_index+1
    return nest, nest_index

    
def separate_sections(block):
    '''

    Parameters
    ----------
    block : string
        HTML text which contains loose text and/or nests

    Raises
    ------
    Exception
        When an else block is found which could not be associated with an if-block in any section

    Returns
    -------
    sections : list of strings
        List of sections derived by separating out the loose text from the nests

    '''
    sections = []
    nest_start = re.search(r'\{\{#tag:tabber', block)
    if nest_start is None:
        sections.append(block)
    else:
        rem = block
        while(rem):
            if(nest_start is None):
                sections.append(rem)
                rem = ''
            else:
                sections.append(rem[:nest_start.start()])
                complete_block, index = get_complete_section(rem,nest_start)
                sections.append(complete_block)
                rem = rem[index:]
                nest_start = re.search(r'\{\{#tag:tabber', rem)
    for section in sections:
        if not has_nests(section) and has_elses(section):
            raise Exception('Unbound elses found in section %s', section)
    return sections
        

def get_else_blocks(complete_section):
    '''

    Parameters
    ----------
    complete_section : string
        HTML text corresponding to a nest enclosed in {{#tag:tabber ... }}.
                                                        
    Returns
    -------
    else_blocks : list of strings
        List of alternatives as indicated by if-else blocks

    '''
    if not has_nests(complete_section):
        raise Exception('No nests in this section')
    if not is_complete_section(complete_section):
        raise Exception('Section is not complete')
    
    else_blocks = []
    
    else_start = re.search(r'\{\{!\}\}\-\{\{!\}\}', complete_section)

    if else_start is None:
        else_blocks.append(complete_section) 
        return else_blocks
        
    nest_start = re.search(r'\{\{#tag:tabber', complete_section) 
    current_block = complete_section[:nest_start.end()]
    rem = complete_section[nest_start.end():]
    else_start = re.search(r'\{\{!\}\}\-\{\{!\}\}', rem)
    

    while(else_start is not None):
        
        nest_start = re.search(r'\{\{#tag:tabber', rem)
       


        done = False
        while(not done):
                if nest_start is None or else_start is None or nest_start.start()>else_start.start():
                    if else_start is None:
                        current_block = current_block + rem
                        rem = ''
                    else:                        
                        current_block = current_block + rem[:else_start.start()]
                        rem = rem[else_start.start():]
                        nest_start = re.search(r'\{\{#tag:tabber', rem) 
                        else_start = re.search(r'\{\{!\}\}\-\{\{!\}\}', rem)
                    done = True
                else:
                    current_block = current_block + rem[:nest_start.start()]
                    nest, index = get_complete_section(rem, nest_start)
                    current_block = current_block + nest
                    rem = rem[index+1:]
                    nest_start = re.search(r'\{\{#tag:tabber', rem) 
                    else_start = re.search(r'\{\{!\}\}\-\{\{!\}\}', rem)
            
                

        else_blocks.append(current_block)
        if else_start is not None:
            current_block = rem[:else_start.end()]
            rem = rem[else_start.end():]
            else_start = re.search(r'\{\{!\}\}\-\{\{!\}\}', rem) 
        
    if rem:
        current_block = current_block + rem
        else_blocks.append(current_block)
    return else_blocks
    
    
def unpack(section):
    '''
    Recursively unpacks section containing nests and else blocks into a structured list of lists
    Parameters
    ----------
    section : string
        HTML text which contains loose text and/or nests (Level 2 sections or upwards - use get_level_1_blocks and get_else_blocks to get level 2 sections)


    Returns
    -------
    unpacked: List of lists
        upacked list

    '''
    if not has_nests(section):
        return section
    else:
        unpacked = []
        else_blocks = get_else_blocks(section)
        for block in else_blocks:                    
            if block.startswith('{{#tag:tabber') :
                 block = block.replace('{{#tag:tabber','IF_BLOCK',1)
            elif block.startswith('{{!}}-{{!}}'):
                block = block.replace('{{!}}-{{!}}','ELSE_BLOCK',1)
            else:
                raise Exception('Unknown block type %s',block)
                
           
            sections = separate_sections(block)
            for section in sections:
                unpacked.append(unpack(section))
    return unpacked

    
def get_parse_tree(dev):
    '''
    Parameters
    ----------
     dev : string 
    a section of the script enclosed by <tabber> </tabber> representing non linear if-else structure where else-blocks are separated using ||-||

    Returns
    -------
    tree : List of lists
        upacked list where all nests and else blocks are converted into a structured list of lists

    '''
    tree=[]
    level_1_blocks = get_level_1_blocks(dev)
    for block in level_1_blocks:

        sections = separate_sections(block)

        for section in sections:
            tree.append(unpack(section))
    return tree

def clean(s):
    '''
    Parameters
    ----------
     s : string 
    text from which html tags need to be removed
    Returns
    -------
    s : string
        string after unnecessary html tags are removed and useful ones are replaced with more readable tags

    '''
    h_pattern = r'(.*)?=<h5 style="display:none">(.*)</h5>'
    while( re.search(h_pattern,s) is not None):
        heading = re.search(h_pattern,s)
        s = s.replace(heading.group(0),'#HEADING#'+heading.group(1)+'#HEADING#')
    h_pattern = r'<tabber>(.*?)=<blockquote>'
    while( re.search(h_pattern,s) is not None):
        heading = re.search(h_pattern,s)
        s = s.replace(heading.group(0),'#HEADING#'+heading.group(1)+'#HEADING#')
    h_pattern = r'#tag:tabber|(.*?)=<blockquote>'
    while( re.search(h_pattern,s) is not None):
        heading = re.search(h_pattern,s)
        s = s.replace(heading.group(0),'#HEADING#'+heading.group(1)+'#HEADING#')
    s = s.replace('</blockquote>','')
    s = s.replace('<tabber>','')
    s = s.replace('</tabber>','')
    s = s.replace('IF_BLOCK','')
    s = s.replace('ELSE_BLOCK','')

    return s
    

def clean_tree(tree):
    c_tree=[]
    for node in tree:
        if type(node) is list:
            c_tree.append(clean_tree(node))
        else:
            c_tree.append(clean(node))
    return c_tree


def get_headings(tree):
    parsed_nodes = {}
    current_node = []
    pattern = '#HEADING#(.*)#HEADING#'
    current_heading = 'START'
    for index,node in enumerate(tree):
        if type(node) is list:
            parsed_tree = get_headings(node)
            current_node.append(parsed_tree)
        elif '#HEADING#' in node:
            match =  re.search(pattern, node)
            current_heading = match.group(1)
            current_node = [node.replace( match.group(0),"CHOICE: "+ match.group(1))]
        else:
            current_node.append(node) 
            
        if current_heading.startswith("|"):
                        current_heading = current_heading[1:]
        if index+1 >= len(tree) or '#HEADING#' in tree[index+1]:
            if current_node:
                parsed_nodes[current_heading] = current_node
    

    parsed_nodes[current_heading] = current_node
    return parsed_nodes
    

def get_parsed_script(script):    
    parsed_script=[]
    
    sections = re.split(r'(==.*==|<u>.*</u>)',script)
    while('==' not in sections[0]):
        sections = sections[1:]
        
    scenes=[]
    scene_texts=[]
    for section in sections:
        if '==' in section or '<u>' in section:
            scenes.append(section)
        else:
            scene_texts.append(section)
    sections=[]
    for scene, scene_text in zip(scenes,scene_texts):
        parsed_scene = []
        sections = re.split(r'(<tabber.*?/tabber>)',scene_text,flags=re.DOTALL)

        for section in sections:
            if (re.match(r'(<tabber.*?/tabber>)',section, flags=re.DOTALL) is not None or 'tag:tabber' in section):
                tree = get_parse_tree(section)
                ctree = clean_tree(tree)
                htree = get_headings(ctree)
                parsed_scene.append(htree)
            else:
                parsed_scene.append(section)
        entry ={}
        entry['name']=scene
        entry['content']=parsed_scene
        parsed_script.append(entry)
    return parsed_script  

    