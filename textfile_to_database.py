'''
Created on Apr 7, 2013

@author: Tony
'''

def get_emotion_ratios(f):
    '''Maps emotions to ratios'''
    emotion_ratios = {}
    line = f.readline().rstrip('\n')
    while line != "END EMOTION RATIOS":
        #lines are structured like so: :) = 1
        line_tokens = line.split(" ")
        emotion = line_tokens[0]
        ratio = line_tokens[2]
        emotion_ratios[emotion] = ratio
        line = f.readline().rstrip('\n')
    return emotion_ratios

def get_adjectives(f):
    '''Maps emotions to adjectives'''
    adjectives = {}
    current_emotion = ""
    line = f.readline().rstrip('\n')
    while line != "END ADJECTIVES":
        #ignore blank lines
        if line == "":
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

def get_adverbs(f):
    '''Maps emotions to adjectives'''
    adverbs = {}
    current_emotion = ""
    line = f.readline().rstrip('\n')
    while line != "END ADVERBS":
        #ignore blank lines
        if line == "":
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
        #ignore blank lines
        if line == "":
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
        #ignore blank lines
        if line == "":
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

def get_tweet_dictionary(f):
    '''Maps keys to tweets'''
    tweet_dictionary = {}
    current_key = ""
    line = f.readline().rstrip('\n')
    while line != "END TWEET DICTIONARY":
        #ignore blank lines
        if line == "":
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

f = open("test_database.txt", "r")
line = f.readline().rstrip('\n')
while line != "END SCRIPT":
    #ignore comments
    if line == "***BEGIN COMMENT***":
        line = f.readline().rstrip('\n')
        while line != "***END COMMENT***":
            line = f.readline().rstrip('\n')
        line = f.readline().rstrip('\n')
    #ignore blank lines
    if line == "":
        line = f.readline().rstrip('\n')
        continue
    
    #use the line to determine what to do
    print(line)
    if line == "EMOTION RATIOS":
        emotion_ratios = get_emotion_ratios(f)
        print(emotion_ratios)
    elif line == "ADJECTIVES":
        adjectives = get_adjectives(f)
        print(adjectives)
    elif line == "ADVERBS":
        adverbs = get_adverbs(f)
        print(adverbs)
    elif line == "HASHTAG GENERIC":
        hashtag_generic = get_hashtag_generic(f)
        print(hashtag_generic)
    elif line == "HASHTAG EMOTION":
        hashtag_emotion = get_hashtag_emotion(f)
        print(hashtag_emotion)
    elif line == "TWEET DICTIONARY":
        tweet_dictionary = get_tweet_dictionary(f)
        print(tweet_dictionary)
    line = f.readline().rstrip('\n')
f.close()
