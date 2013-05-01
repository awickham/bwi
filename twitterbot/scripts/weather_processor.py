from textfile_to_database import weather_positive, weather_negative, weather_neutral, emotion_ratios
from twitter_database import get_high_temp, get_low_temp, get_current_temp, get_precip_inches, get_precip_amount, get_cloud_coverage_percent, get_sky_description, get_humidity, get_weather_description, parse_tweet
from random import choice, randint

POSITIVE = 0
NEGATIVE = 1

positive_params = []
negative_params = []

'''weather_params = ["<high-temp>", "<low-temp>", "<current-temp>", "<precip-inches>", "<precip-amount>", "<cloud-coverage-percent>", "<sky-description>", "<humidity>", "<weather-description>"]'''

def decide_positive_or_negative():
	'''Decides whether to tweet positvely or negatively about the weather.
	This decision is based on aspects of the weather and emotion ratios.'''
	global positive_params
	global negative_params
	positive_params = []
	negative_params = []
	
	high_temp = int(get_high_temp())
	if high_temp > 60 and high_temp < 85:
		positive_params.append("<high-temp>")
	else:
		negative_params.append("<high-temp>")

	low_temp = int(get_low_temp())
	if low_temp > 40 and low_temp < 75:
		positive_params.append("<low-temp>")
	else:
		negative_params.append("<low-temp>")

	current_temp = int(get_current_temp())
	if current_temp > 60 and current_temp < 85:
		positive_params.append("<current-temp>")
	else:
		negative_params.append("<current-temp>")

	precip_inches = float(get_precip_inches())
	if precip_inches == 0:
		positive_params.append("<precip-inches>")
		positive_params.append("<precip-amount>")
	else:
		negative_params.append("<precip-inches>")
		negative_params.append("<precip-amount>")

	cloud_coverage_percent = int(get_cloud_coverage_percent())
	if cloud_coverage_percent <= 50:
		positive_params.append("<cloud-coverage-percent>")
		positive_params.append("<sky-description>")
	else:
		negative_params.append("<cloud-coverage-percent>")
		negative_params.append("<sky-description>")

	'''Deciding whether humidity is negative depends on temperature.
	Thus, we created a crude formula for uncomfortability: 4000 / temp = minimum uncomfortable humidity
	(If it is only 40 degrees out, it can be 100% humid and not be bad; if it is 100 degrees, 40% is uncomfortable)'''
	humidity = int(get_humidity())
	temp = int(get_current_temp())
	if 4000 / temp >= humidity:
		positive_params.append("<humidity>")
	else:
		negative_params.append("<humidity>")
	
	positive_emotions_sum = int(emotion_ratios[":)"]) + int(emotion_ratios[":D"]) + int(emotion_ratios["<3"])
	negative_emotions_sum = int(emotion_ratios[":("]) + int(emotion_ratios[":'("]) + int(emotion_ratios[">:("])

	positive = positive_emotions_sum * len(positive_params)
	negative = negative_emotions_sum * len(negative_params)

	if randint(1, positive + negative) <= positive:
		return POSITIVE
	else:
		return NEGATIVE

def tweet_neutrally_about_weather():
	return parse_tweet(choice(weather_neutral))

def tweet_positively_about_weather():
	positive_tweets = []
	global positive_params
	global negative_params
	for param in positive_params:
		if param in weather_positive:
			for tweet in weather_positive[param]:
				#don't include this tweet if it contains a negative parameter
				for neg_param in negative_params:
					if tweet.find(neg_param) != -1:
						break #continue outer for loop
				else:
					positive_tweets.append(tweet)
	if len(positive_tweets) == 0:
		return tweet_neutrally_about_weather()
	else:
		return parse_tweet(choice(positive_tweets))

def tweet_negatively_about_weather():
	negative_tweets = []
	global positive_params
	global negative_params
	for param in negative_params:
		if param in weather_negative:
			for tweet in weather_negative[param]:
				#don't include this tweet if it contains a positive parameter
				for pos_param in positive_params:
					if tweet.find(pos_param) != -1:
						break #continue outer for loop
				else:
					negative_tweets.append(tweet)
	if len(negative_tweets) == 0:
		return tweet_neutrally_about_weather()
	else:
		return parse_tweet(choice(negative_tweets))

def tweet_about_weather():
	'''Uses all the above code to decide what to tweet about data'''
	feeling_about_weather = decide_positive_or_negative()
	if feeling_about_weather == POSITIVE:
		return tweet_positively_about_weather()
	elif feeling_about_weather == NEGATIVE:
		return tweet_negatively_about_weather()
	else:
		return tweet_neutrally_about_weather()
