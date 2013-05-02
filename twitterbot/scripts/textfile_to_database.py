'''
Created on Apr 7, 2013

@author: Tony
'''

import os
import urllib2

url_of_twitter_database_txt = 'https://github.com/awickham/bwi/raw/master/twitterbot/scripts/twitter_database.txt'

emotion_ratios = {}
adjectives_cause = {}
adjectives_effect = {}
adverbs = {}
hashtag_generic = []
hashtag_emotion = {}
tweet_dictionary = {}

#weather stuff
weather_positive = {}
weather_negative = {}
weather_neutral = {}
weather_params = ["<high-temp>", "<high-temp-cold>", "<high-temp-hot>", "<low-temp>", "<low-temp-cold>", "<low-temp-hot>", "<current-temp>", "<current-temp-cold>", "<current-temp-hot>", "<precip-inches>", "<precip-amount>", "<cloud-coverage-percent>", "<sky-description>", "<humidity>", "<weather-description>"]

def get_emotion_ratios(f):
    '''Maps emotions to ratios'''
    emotion_ratios = {}
    line = f.readline().rstrip('\n')
    while line != "END EMOTION RATIOS":
	#ignore blank lines or single-line comments
    	if line == "" or (len(line) >= 2 and line[0:2] == "//"):
            line = f.readline().rstrip('\n')
            continue
        #lines are structured like so: :) = 1
        line_tokens = line.split(" ")
        emotion = line_tokens[0]
        ratio = line_tokens[2]
        emotion_ratios[emotion] = ratio
        line = f.readline().rstrip('\n')
    return emotion_ratios

def get_adjectives_cause(f):
    '''Maps emotions to adjectives'''
    adjectives = {}
    current_emotion = ""
    line = f.readline().rstrip('\n')
    while line != "END ADJECTIVES-CAUSE":
        #ignore blank lines or single-line comments
    	if line == "" or (len(line) >= 2 and line[0:2] == "//"):
            line = f.readline().rstrip('\n')
            continue
        if line[:10] == "Emotion = ":
            current_emotion = line[10:]
            #create dictionary entry for this emotion
            adjectives[current_emotion] = []
        else:
            #add this line to the list of definitions for the emotion
            adjectives[current_emotion].append(line)
        line = f.readline().rstrip('\n')
    return adjectives

def get_adjectives_effect(f):
    '''Maps emotions to adjectives'''
    adjectives_effect = {}
    current_emotion = ""
    line = f.readline().rstrip('\n')
    while line != "END ADJECTIVES-EFFECT":
        #ignore blank lines or single-line comments
    	if line == "" or (len(line) >= 2 and line[0:2] == "//"):
            line = f.readline().rstrip('\n')
            continue
        if line[:10] == "Emotion = ":
            current_emotion = line[10:]
            #create dictionary entry for this emotion
            adjectives_effect[current_emotion] = []
        else:
            #add this line to the list of definitions for the emotion
            adjectives_effect[current_emotion].append(line)
        line = f.readline().rstrip('\n')
    return adjectives_effect

def get_adverbs(f):
    '''Maps emotions to adjectives'''
    adverbs = {}
    current_emotion = ""
    line = f.readline().rstrip('\n')
    while line != "END ADVERBS":
        #ignore blank lines or single-line comments
    	if line == "" or (len(line) >= 2 and line[0:2] == "//"):
            line = f.readline().rstrip('\n')
            continue
        if line[:10] == "Emotion = ":
            current_emotion = line[10:]
            #create dictionary entry for this emotion
            adverbs[current_emotion] = []
        else:
            #add this line to the list of definitions for the emotion
            adverbs[current_emotion].append(line)
        line = f.readline().rstrip('\n')
    return adverbs

def get_hashtag_generic(f):
    '''Lists generic hashtags'''
    hashtag_generic = []
    line = f.readline().rstrip('\n')
    while line != "END HASHTAG GENERIC":
        #ignore blank lines or single-line comments
    	if line == "" or (len(line) >= 2 and line[0:2] == "//"):
            line = f.readline().rstrip('\n')
            continue
        hashtag_generic.append(line)
        line = f.readline().rstrip('\n')
    return hashtag_generic

def get_hashtag_emotion(f):
    '''Maps emotions to hashtags'''
    hashtag_emotion = {}
    current_emotion = ""
    line = f.readline().rstrip('\n')
    while line != "END HASHTAG EMOTION":
        #ignore blank lines or single-line comments
    	if line == "" or (len(line) >= 2 and line[0:2] == "//"):
            line = f.readline().rstrip('\n')
            continue
        if line[:10] == "Emotion = ":
            current_emotion = line[10:]
            #create dictionary entry for this emotion
            hashtag_emotion[current_emotion] = []
        else:
            #add this line to the list of definitions for the emotion
            hashtag_emotion[current_emotion].append(line)
        line = f.readline().rstrip('\n')
    return hashtag_emotion

def get_weather_positive(f):
    '''Maps weather parameters to positive tweets'''
    weather_positive = {}
    line = f.readline().rstrip('\n')
    while line != "END WEATHER POSITIVE":
	#ignore blank lines or single-line comments
    	if line == "" or (len(line) >= 2 and line[0:2] == "//"):
            line = f.readline().rstrip('\n')
            continue
	#loop through list of weather params and map them to tweets that use them
	global weather_params
	for param in weather_params:
	    if line.find(param) == -1:
		continue
	    else:
		if param not in weather_positive.keys():
		    weather_positive[param] = []
		weather_positive[param].append(line)
	line = f.readline().rstrip('\n')
    return weather_positive

def get_weather_negative(f):
    '''Maps weather parameters to negative tweets'''
    weather_negative = {}
    line = f.readline().rstrip('\n')
    while line != "END WEATHER NEGATIVE":
	#ignore blank lines or single-line comments
    	if line == "" or (len(line) >= 2 and line[0:2] == "//"):
            line = f.readline().rstrip('\n')
            continue
	#loop through list of weather params and map them to tweets that use them
	global weather_params
	for param in weather_params:
	    if line.find(param) == -1:
		continue
	    else:
		if param not in weather_negative.keys():
		    weather_negative[param] = []
		weather_negative[param].append(line)
	line = f.readline().rstrip('\n')
    return weather_negative

def get_weather_neutral(f):
    '''Lists neutral tweets about the weather'''
    weather_neutral = []
    line = f.readline().rstrip('\n')
    while line != "END WEATHER NEUTRAL":
	#ignore blank lines or single-line comments
    	if line == "" or (len(line) >= 2 and line[0:2] == "//"):
            line = f.readline().rstrip('\n')
            continue
	weather_neutral.append(line)
	line = f.readline().rstrip('\n')
    return weather_neutral

def get_tweet_dictionary(f):
    '''Maps keys to tweets'''
    tweet_dictionary = {}
    current_key = ""
    line = f.readline().rstrip('\n')
    while line != "END TWEET DICTIONARY":
        #ignore blank lines or single-line comments
    	if line == "" or (len(line) >= 2 and line[0:2] == "//"):
            line = f.readline().rstrip('\n')
            continue
        if line[:6] == "Key = ":
            current_key = line[6:]
            #create dictionary entry for this key
            tweet_dictionary[current_key] = []
        else:
            #add this line to the list of tweets for the key
            tweet_dictionary[current_key].append(line)
        line = f.readline().rstrip('\n')
    return tweet_dictionary

'''Parse the twitter_database.txt file from GitHub'''
f = urllib2.urlopen(url_of_twitter_database_txt)
line = f.readline().rstrip('\n')
while line != "END SCRIPT":
    #ignore comment blocks
    if line == "***BEGIN COMMENT***":
        line = f.readline().rstrip('\n')
        while line != "***END COMMENT***":
            line = f.readline().rstrip('\n')
        line = f.readline().rstrip('\n')
    #ignore blank lines or single-line comments
    if line == "" or (len(line) >= 2 and line[0:2] == "//"):
        line = f.readline().rstrip('\n')
        continue

    #use the line to determine what to do
    #print(line)
    if line == "EMOTION RATIOS":
        emotion_ratios = get_emotion_ratios(f)
        #print(emotion_ratios)
    elif line == "ADJECTIVES-CAUSE":
        adjectives_cause = get_adjectives_cause(f)
        #print(adjectives_cause)
    elif line == "ADJECTIVES-EFFECT":
        adjectives_effect = get_adjectives_effect(f)
        #print(adjectives_effect)
    elif line == "ADVERBS":
        adverbs = get_adverbs(f)
        #print(adverbs)
    elif line == "HASHTAG GENERIC":
        hashtag_generic = get_hashtag_generic(f)
        #print(hashtag_generic)
    elif line == "HASHTAG EMOTION":
        hashtag_emotion = get_hashtag_emotion(f)
        #print(hashtag_emotion)
    elif line == "WEATHER POSITIVE":
	weather_positive = get_weather_positive(f)
	#print(weather_positive)
    elif line == "WEATHER NEGATIVE":
	weather_negative = get_weather_negative(f)
	#print(weather_negative)
    elif line == "WEATHER NEUTRAL":
	weather_neutral = get_weather_neutral(f)
	#print(weather_neutral)
    elif line == "TWEET DICTIONARY":
        tweet_dictionary = get_tweet_dictionary(f)
        #print(tweet_dictionary)
    line = f.readline().rstrip('\n')
f.close()
