import re
def remove_html_tags(s):
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