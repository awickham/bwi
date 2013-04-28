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

'''emotion_ratio, adjectives_cause, adjectives_effect, adverbs, hashtag-generic,
hashtag-emotion, and tweet_dictionary set by textfile_to_database.py'''

emotions = list(emotion_ratios.keys())

#stores text contained in quotes
quotes = []

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
def get_hashtag_emotion():
    global hashtag_emotion
    global current_emotion
    if current_emotion == "":
        current_emotion = set_emotion()
    #choose random adj based on emotion
    possible_hashtags = hashtag_emotion[current_emotion]
    return choice(possible_hashtags)

'''Returns a body of text, possibly based on emotions'''
def parse_text(options, *params):
    #note: assuming options are all plain text or all based on emotions
    first_char = options[0][0]
    if first_char == '"': #dealing with plain text; pick one at random
        return 
    
'''Returns a param from a list of passed params'''
def get_param(param_index_and_name, *params):
    equal_index = param_index_and_name.find("=")
    #if '=' isn't found, the param has no name
    param_index = int(param_index_and_name) if equal_index == -1 else int(param_index_and_name[:equal_index])
    return params[param_index]

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
def parse_token(token, *params):
    #nothing to parse if not a token
    if not is_dynamic(token):
        return token
    #remove < and >
    index_open = token.find("<")
    index_close = token.find(">")
    str_before = token[:index_open]
    str_after = ""
    #if there is text after the ">", save it in str_after
    if len(token) > index_close + 1:
        str_after = token[index_close + 1:]
    token = token[index_open + 1:index_close]
    
    #if there are any |'s pick a token at random
    token = choice(token.split("|"))
    #omit token if blank
    if token == "":
        return ""
    
    token_components = token.split("_")
    token_type = token_components[0]
    if token_type == "param":
        return str_before + get_param(token_components[1], *params) + str_after
    elif token_type == "text":
        if len(token_components) == 1: #there are no parameters
            return "<text>"
        return str_before + parse_text(token_components[1:], *params) + str_after
    elif len(token_components) > 1: #there are specified emotions to choose from
        global current_emotion
        current_emotion = choice(token_components[1:])
    if token_type in translated_token: #token is defined
        #get function to generate token content
        transform_token = translated_token[token_type]
        return str_before + transform_token() + str_after
    #token undefined
    return str_before + "<" + token + ">" + str_after

'''Replaces text in quotes with a dynamic token <quote_index> that refers to
quotes[index] (which will store the original text)'''
def group_quotes(string):
    x = 0
    length = len(string)
    while x < length:
        if string[x] == '"': #found opening quotation mark
            #store index of closing quotation mark
            close_index = string[x + 1:].find('"') + x + 1
            if close_index == -1: #there's no closing quote
                break
            else:
                dynamic_token = "<quote-" + str(len(quotes)) + ">"
                #add text to quotes list, including quotation marks
                quotes.append(string[x:close_index + 1])
                #replace text with dynamic token
                string = string[:x] + dynamic_token + string[close_index + 1:]
                #skip over new token
                x += len(dynamic_token)
                #reset length
                length = len(string)
        else:
            x += 1
    return string

'''Iterates over and parses the tokens (words) of the given string. If the word
"a" is followed by a dynamic token, that token is parsed to determine if it
should be changed to "an"'''
def parse_tweet(tweet, *params):
    if len(tweet) == 0:
        return ""
    global current_emotion
    current_emotion = ""
    tweet = group_quotes(tweet)
    tokens = tweet.split(" ")
    parsed_tweet = ""
    for i, x in enumerate(tokens):
        if x == '':
            continue
        #don't have space before first token (still need to compute it here in
        #case the first token is "a")
        if i == 0:
            space = ""
        else:
            space = " "
        if (x == "a" or x == "A") and len(tokens) > i + 1:
            #determine if we should make it 'an' by computing next token
            tokens[i + 1] = parse_token(tokens[i + 1], *params)
            if tokens[i + 1] == "":
                parsed_tweet += space + x #x is "a" or "A"
            elif tokens[i + 1][0] in "AEIOUaeiou":
                #keep case
                if x == "a": 
                    parsed_tweet += space + "an"
                else:
                    parsed_tweet += space + "An"
            else:
                parsed_tweet += space + x #x is "a" or "A"
        else:
            token = parse_token(x, *params)
            #don't have a space for blank or initial token
            if token != "":
                parsed_tweet += space + token
    return parsed_tweet

print parse_tweet('<test_"hi there"_"bye there">')