from random import *
from textfile_to_database import *

'''
Created on Apr 6, 2013

@author: Andy and Tony
'''

'''TODO: Gets trending topics as hashtags from Twitter'''
def get_trending_topics():
    return ["hi", 
            "bye"]
    
current_emotion = ""

'''emotion_ratio, adjectives_cause, adjectives_effect, adverbs, hashtag_generic,
hashtag_emotion, and tweet_dictionary set by textfile_to_database.py'''

emotions = list(emotion_ratios.keys())

'''Resets the current emotion based on their ratios'''
def set_emotion():
    global emotion_ratios
    global current_emotion
    global emotions
    #the index of the chosen emotion will be >= the random number chosen,
    #which must be greater than the ranges below it
    emotion_ranges = [int(emotion_ratios[emotions[0]])]
    #each range corresponds to an emotion here
    corresponding_emotions = [emotions[0]]
    for emotion in emotions[1:]:
        emotion_ranges.append(int(emotion_ranges[-1]) + int(emotion_ratios[emotion]))
        corresponding_emotions.append(emotion)
    random = randint(emotion_ranges[0], emotion_ranges[-1])
    #anything set to 0 odds should not have a chance to be picked
    if random == 0:
        random = 1
    for i, x in enumerate(emotion_ranges):
        if x >= random:
            return corresponding_emotions[i]

'''Picks an adjective (cause) correlated to one of the given emotions, based on their ratios'''
def get_adjective_cause():
    global adjectives_cause
    global current_emotion
    if current_emotion == "":
        current_emotion = set_emotion()
    #choose random adj based on emotion
    possible_adjs = adjectives_cause[current_emotion]
    return choice(possible_adjs)

'''Picks an adjective (effect) correlated to one of the given emotions, based on their ratios'''
def get_adjective_effect():
    global adjectives_effect
    global current_emotion
    if current_emotion == "":
        current_emotion = set_emotion()
    #choose random adj based on emotion
    possible_adjs = adjectives_effect[current_emotion]
    return choice(possible_adjs)

'''Picks an adverb correlated to one of the given emotions, based on their ratios'''
def get_adverb():
    global adverbs
    global current_emotion
    if current_emotion == "":
        current_emotion = set_emotion()
    #choose random adv based on emotion
    possible_advs = adverbs[current_emotion]
    return choice(possible_advs)

'''Picks an emoticon from a list of possible emotions, based on their ratios'''
def get_emoticon():
    global adjectives
    global current_emotion
    if current_emotion == "":
        current_emotion = set_emotion()
    return current_emotion

'''Picks a generic hashtag at random'''
def get_hashtag_generic():
    global hashtag_generic
    return choice(hashtag_generic)

'''Picks a hashtag correlated to one of the given emotions, based on their ratios'''
def get_hastag_emotion():
    global hashtag_emotion
    global current_emotion
    if current_emotion == "":
        current_emotion = set_emotion()
    #choose random adj based on emotion
    possible_hashtags = hashtag_emotion[current_emotion]
    return choice(possible_hashtags)

'''Maps dynamic tokens to functions that generate their content'''
translated_token = {"adj-cause": get_adjective_cause,
		    "adj-effect": get_adjective_effect,
		    "adv": get_adverb,
                    "emoticon": get_emoticon,
		    "hashtag-generic": get_hashtag_generic,
		    "hashtag-emotion": get_hashtag_emotion}

'''Determines if the given token is enclosed by < and >'''
def is_dynamic(token):    
    return len(token) > 0 and token.find("<") != -1 and token.find(">") != -1

'''If the token is dynamic, this replaces it with an adjective, emoticon,
etc. accordingly'''
def parse_token(token):
    #nothing to parse if not a token
    if not is_dynamic(token):
        return token
    #remove < and >
    index_open = token.find("<")
    index_close = token.find(">")
    str_before = token[:index_open]
    str_after = ""
    if len(token) > index_close + 1:
        str_after = token[index_close + 1:]
    token = token[index_open + 1:index_close]
    
    token_components = token.split("_")
    token_type = token_components[0]
    if len(token_components) > 1: #there are specified emotions to choose from
        global current_emotion
        current_emotion = choice(token_components[1:])
    if token_type in translated_token: #token is defined
        #get function to generate token content
        transform_token = translated_token[token_type]
        return str_before + transform_token() + str_after
    #token undefined
    return str_before + "<" + token + ">" + str_after

'''Iterates over and parses the tokens (words) of the given string. If the word
"a" is followed by a dynamic token, that token is parsed to determine if it
should be changed to "an"'''
def parse_tweet(tweet):
    if len(tweet) == 0:
        return ""
    global current_emotion
    current_emotion = ""
    tokens = tweet.split(" ")
    parsed_tweet = parse_token(tokens[0])
    tokens = tokens[1:]
    for i, x in enumerate(tokens):
        if x == '':
            continue
        if x == "a":
            #determine if we should make it 'an'
            #note: assuming we won't end a tweet with 'a'
            tokens[i + 1] = parse_token(tokens[i + 1])
            if tokens[i + 1][0] in "AEIOUaeiou":
                parsed_tweet += " an"
            else:
                parsed_tweet += " a"
        else: parsed_tweet += " " + parse_token(x)
    return parsed_tweet
