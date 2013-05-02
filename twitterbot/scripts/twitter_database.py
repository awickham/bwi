from random import *
from textfile_to_database import emotion_ratios, adjectives_cause, adjectives_effect, adverbs, hashtag_generic, hashtag_emotion, tweet_dictionary
import weather_node

'''
Created on Apr 6, 2013

@author: Andy and Tony
'''

current_emotion = ""


emotions = list(emotion_ratios.keys())

#stores text contained in quotes
quotes = []

'''TODO: Gets trending topics as hashtags from Twitter'''
def get_trending_topics():
    return ["hi", 
            "bye"]

def get_high_temp():
    return str(weather_node.high)

def get_low_temp():
    return str(weather_node.low)

def get_current_temp():
    return str(weather_node.current_temp())

def get_precip_inches():
    return str(weather_node.curr_precip_inches())

def get_precip_amount():
    '''precip_amount is defined as something that makes sense in this context: "There is <precip-amount> rain today."'''
    precip_inches = weather_node.curr_precip_inches()
    if precip_inches == 0:
        return choice(["no", "not a drop of", "absolutely no"])
    elif precip_inches < 0.6:
        return choice(["a little", "some"])
    elif precip_inches < 1.0:
        return choice(["a fair amount of", "a bit of", "moderate amounts of", "an unpleasant amount of"])
    else:
        return choice(["way too much", "heavy amounts of", "so much", "tons of"])

def get_cloud_coverage_percent():
    return str(weather_node.cloudcover())

def get_sky_description():
    '''The sky is <sky-description>. (or) The <sky-description> sky ....'''
    cloud_coverage_percent = int(get_cloud_coverage_percent())
    if cloud_coverage_percent <= 25:
        return choice(["sunny", "clear"])
    elif cloud_coverage_percent <= 50:
        return choice(["mostly sunny"])
    elif cloud_coverage_percent <= 75:
        return choice(["partly cloudy"])
    else:
        return choice(["mostly cloudy", "overcast", "dark"])

def get_humidity():
    return str(weather_node.humidity())

def get_wind_speed():
	return str(weather_node.windSpeed())

def get_weather_description():
    return weather_node.curr_weatherDesc()

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
            current_emotion = corresponding_emotions[i]
            return

'''Uses emotion ratios to set current_emotion to one from the passed list'''        
def set_emotion_from_list(list):
    global emotions
    temp = emotions
    #set possible emotions to be only those in the list
    emotions = list
    set_emotion()
    #restore emotions to complete list
    emotions = temp

'''Picks an adjective (cause) correlated to one of the given emotions, based on their ratios'''
def get_adjective_cause():
    global adjectives_cause
    global current_emotion
    if current_emotion == "":
        set_emotion()
    #choose random adj based on emotion
    possible_adjs = adjectives_cause[current_emotion]
    return choice(possible_adjs)

'''Picks an adjective (effect) correlated to one of the given emotions, based on their ratios'''
def get_adjective_effect():
    global adjectives_effect
    global current_emotion
    if current_emotion == "":
        set_emotion()
    #choose random adj based on emotion
    possible_adjs = adjectives_effect[current_emotion]
    return choice(possible_adjs)

'''Picks an adverb correlated to one of the given emotions, based on their ratios'''
def get_adverb():
    global adverbs
    global current_emotion
    if current_emotion == "":
        set_emotion()
    #choose random adv based on emotion
    possible_advs = adverbs[current_emotion]
    return choice(possible_advs)

'''Picks an emoticon from a list of possible emotions, based on their ratios'''
def get_emoticon():
    global adjectives
    global current_emotion
    if current_emotion == "":
        set_emotion()
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
        set_emotion()
    #choose random adj based on emotion
    possible_hashtags = hashtag_emotion[current_emotion]
    return choice(possible_hashtags)

'''Returns a body of text, possibly based on emotions'''
def parse_text(options, *params):
    global current_emotion
    #note: assuming options are all plain text or all based on emotions (not mixed)
    first_char = options[0][0]
    if first_char == '"': #dealing with plain text
        #pick one at random and remove quotation marks
        return parse_token(choice(options))[1:-1]
    else:
        dictionary = {}
        for x in options:
            equal_index = x.find("=")
            emotion = x[:equal_index]
            #remove quotes from text
            text = x[equal_index + 2:-1]
            dictionary[emotion] = text
        set_emotion_from_list(dictionary.keys())
        return parse_token(dictionary[current_emotion])
    
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
            "hashtag-emotion": get_hashtag_emotion,
            "high-temp": get_high_temp,
			"high-temp-cold" : get_high_temp,
			"high-temp-hot" : get_high_temp,
            "low-temp": get_low_temp,
			"low-temp-cold" : get_low_temp,
			"low-temp-hot" : get_low_temp,
            "current-temp": get_current_temp,
			"current-temp-cold": get_current_temp,
			"current-temp-hot": get_current_temp,
            "precip-inches": get_precip_inches,
            "precip-amount": get_precip_amount,
            "cloud-coverage-percent": get_cloud_coverage_percent,
            "sky-description": get_sky_description,
            "humidity-percent": get_humidity,
			"wind-speed": get_wind_speed,
            "weather-description": get_weather_description}

'''Determines if the given token is enclosed by < and >'''
def is_dynamic(token):    
    return len(token) > 0 and token.find("<") != -1 and token.rfind(">") != -1

'''Determines if the token type (first element of a token delimited by '_') is a quote'''
def is_quote(token_type):
    #must say at least "quote-0" (7 characters) to be a quote token
    if len(token_type) < 7:
        return False
    return token_type[:5] == "quote" and token_type[5] == "-"

'''If the token is dynamic, this replaces it with an adjective, emoticon,
etc. accordingly'''
def parse_token(token, *params):
    global quotes
    global current_emotion
    
    #nothing to parse if not a token
    if not is_dynamic(token):
        return token
    #remove < and >
    index_open = token.find("<")
    index_close = token.rfind(">")
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
    elif is_quote(token_type):
        quote_index = int(token_type[token_type.find('-') + 1:])
        return str_before + quotes[quote_index] + str_after
    elif token_type == "text":
        if len(token_components) == 1: #there are no parameters
            return "<text>"
        return str_before + parse_text(token_components[1:], *params) + str_after
    elif token_type == "set-emotion":
        if len(token_components) == 1: #there are no parameters
            #pick any emotion randomly based on ratios
            set_emotion()
        else:
            emotions = token_components[1:]
            #check if any emotion listed has chance of being picked (i.e. not 0)
            is_chance = False
            for x in emotions:
                global emotion_ratios
                if int(emotion_ratios[x]) > 0:
                    is_chance = True
                    break
            if(is_chance):
                set_emotion_from_list(emotions)
            else:
                current_emotion = choice(emotions)
        return ""
    
    if len(token_components) > 1: #there are specified emotions to choose from
        current_emotion = choice(token_components[1:])
    if token_type in translated_token: #token is defined
        #get function to generate token content
        transform_token = translated_token[token_type]
        return str_before + transform_token() + str_after
    #token undefined, but may contain defined tokens
    return str_before + "<" + parse_token(token, *params) + ">" + str_after

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
                #add text to quotes list, excluding quotation marks
                quotes.append(string[x + 1:close_index])
                #replace text with dynamic token
                string = string[:x + 1] + dynamic_token + string[close_index:]
                #skip over new token
                x += len(dynamic_token) + 2
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
