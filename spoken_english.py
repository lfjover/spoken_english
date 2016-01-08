import numpy as np
import pandas as pd
import re
import os
import pdb

from collections import Counter


def process_chat(file_path):
    chat = []
    print file_path
    with open(file_path) as f:
        for line in f:
            chat.append(line.strip().split('\t'))
    for i,line in enumerate(chat):
        chat[i] = chat[i][0].split() + line[1:] #separate start and end time
        if len(line)>4:
            print i
            print line
            del chat[i]
        else:                               #clean or add person talking
            m = re.search(':',chat[i][2])
            if m:
                chat[i][2] = chat[i][2][:m.start()]
            else:
                chat[i][2] = chat[i-1][2]
    for i,line in enumerate(chat):
    	if len(line)>4:
    		print i
    		print line
    chat = pd.DataFrame(chat)
    chat.columns = ['start_time','end_time','person','speech']
    # clean speech
    chat['clean_speech'] = chat.speech #placeholder
    for i,text in enumerate(chat.clean_speech):
        text = re.sub(r'\[.*\]', '', text)
        text = re.sub(r'\(.*\)', '', text)
        text = re.sub(r'=','',text)
        text = re.sub(r'[^A-Za-z\']',' ',text)
        chat.clean_speech[i] = text.split()
    return chat


def get_list_of_words(clean_speech_series):
    """get list of words from time series of clean speech"""
    
    words = []
    for text in clean_speech_series:
        words = words + text
    return words


if __name__ == '__main__':
	#create a dictionary with all the words
	chat1 = process_chat('data/transcripts/SBC001.trn')
	words = get_list_of_words(chat1.clean_speech)
	word_dict = Counter(words)

	file_names = os.listdir('data/transcripts')
	for file_name in file_names[1:] :
	    chat = process_chat('data/transcripts/'+file_name)
	    word_dict.update(get_list_of_words(chat.clean_speech))