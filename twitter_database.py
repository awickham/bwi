from random import *

'''
Created on Apr 6, 2013

@author: Andy and Tony
'''

'''TODO: Gets trending topics as hashtags from Twitter'''
def get_trending_topics():
    return ["hi", 
            "bye"]
    
current_emotion = ""

emotion_ratios = {":)": 1,
                  ":(": 0}

adjectives = {":)": ["happy", "great", "pleasant", "lovely"],
              ":(": ["sad", "depressing", "unpleasant"]}

tweet_outline = {"turned_on": ["Just woke up. Today is going to be a <adj> day! <emoticon>"],
                 "bored": ["*sigh* I'm just <adv_-.-_:|> sitting here... <emoticon>\n<hashtag_emotion>"],
                 "default": ["I don't have an opinion on this, but everyone else is doing it, so...\n<hashtag_trending>"]}

'''Resets the current emotion based on their ratios'''
def set_emotion(emotions):
    global emotion_ratios
    global current_emotion
    #the index of the chosen emotion will be >= the random number chosen,
    #which must be greater than the ranges below it
    emotion_ranges = [emotion_ratios[emotions[0]]]
    #each range corresponds to an emotion here
    corresponding_emotions = [emotions[0]]
    for emotion in emotions[1:]:
        emotion_ranges.append(emotion_ranges[-1] + emotion_ratios[emotion])
        corresponding_emotions.append(emotion)
    random = randint(emotion_ranges[0], emotion_ranges[-1])
    #anything set to 0 odds should not have a chance to be picked
    if random is 0:
        random = 1
    for i, x in enumerate(emotion_ranges):
        if x >= random:
            current_emotion = corresponding_emotions[i]
            break

'''Picks an adjective correlated to one of the given emotions, based on their ratios'''
def get_adjective(emotion_list):
    global adjectives
    global current_emotion
    if current_emotion == "":
        set_emotion(emotion_list)
    #choose random adj based on emotion
    return choice(adjectives[current_emotion])

'''Picks an emoticon from a list of possible emotions, based on their ratios'''
def get_emoticon(emotion_list):
    global adjectives
    global current_emotion
    if current_emotion == "":
        set_emotion(emotion_list)
    return current_emotion

'''Maps dynamic tokens to functions that generate their content'''
translated_token = {"adj": get_adjective(list(adjectives.keys())),
                    "emoticon": get_emoticon(list(adjectives.keys()))}

'''Determines if the given token is enclosed by < and >'''
def is_dynamic(token):    
    return len(token) > 0 and token[0] == "<" and token[-1] == ">"

'''If the token is dynamic, this replaces it with an adjective, emoticon,
etc. accordingly'''
def parse_token(token):
    #nothing to parse if not a token
    if not is_dynamic(token):
        return token
    #remove < and >
    token = token[1:-1]
    token_components = token.split("_")
    #TODO: allow for specified emotions
    if len(token_components) == 1:
        return translated_token[token_components[0]]

'''Iterates over and parses the tokens (words) of the given string. If the word
"a" is followed by a dynamic token, that token is parsed to determine if it
should be changed to "an"'''
def parse_tweet(tweet):
    if len(tweet) == 0:
        return ""
    global current_emotion
    current_emotion = ""
    tokens = tweet.split(" ")
    parsed_tweet = tokens[0]
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


print( parse_tweet( tweet_outline["turned_on"][0] ) )
