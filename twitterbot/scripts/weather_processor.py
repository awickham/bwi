from textfile_to_database import weather_positive, weather_negative, weather_neutral, emotion_ratios
from twitter_database import get_high_temp, get_low_temp, get_current_temp, get_precip_inches, get_precip_amount, get_cloud_coverage_percent, get_sky_description, get_humidity, get_wind_speed, get_weather_description, parse_tweet
from random import choice, randint

POSITIVE = 0
NEGATIVE = 1
NEUTRAL = 2

positive_params = []
negative_params = []

'''weather_params = ["<high-temp>", "<high-temp-cold>", "<high-temp-hot>", "<low-temp>", "<low-temp-cold>", "<low-temp-hot>", "<current-temp>", "<current-temp-cold>", "<current-temp-hot>", "<precip-inches>", "<precip-amount>", "<cloud-coverage-percent>", "<sky-description>", "<humidity>", "<wind-speed>", "<weather-description>", "<high-temp-cold?>", "<high-temp-hot?>", "<low-temp-cold?>", "<low-temp-hot?>", "<current-temp-cold?>", "<current-temp-hot?>", "<is-rain?>", "<is-clear?>", "<is-overcast?>", "<high-humidity?>", "<low-humidity?>", "<high-wind-speed?>", "<low-wind-speed?>"]'''

def add_boolean_token(bool_token):
	global positive_params
	global negative_params
	positive_params.append(bool_token)
	negative_params.append(bool_token)

def decide_positive_or_negative():
	'''Decides whether to tweet positvely or negatively about the weather.
	This decision is based on aspects of the weather and emotion ratios.'''
	global positive_params
	global negative_params
	positive_params = []
	negative_params = []
	
	high_temp = int(get_high_temp())
	if high_temp >= 70 and high_temp <= 85:
		positive_params.append("<high-temp>")
	else:
		negative_params.append("<high-temp>")
		if high_temp < 70:
			negative_params.append("<high-temp-cold>")
			add_boolean_token("<high-temp-cold?>")
		else: #high_temp > 85
			negative_params.append("<high-temp-hot>")
			add_boolean_token("<high-temp-hot?>")

	low_temp = int(get_low_temp())
	if low_temp >= 45 and low_temp <= 60:
		positive_params.append("<low-temp>")
	else:
		negative_params.append("<low-temp>")
		if low_temp < 45:
			negative_params.append("<low-temp-cold>")
			add_boolean_token("<low-temp-cold?>")
		else: #low_temp > 60
			negative_params.append("<low-temp-hot>")
			add_boolean_token("<low-temp-hot?>")

	current_temp = int(get_current_temp())
	if current_temp >= 70 and current_temp <= 85:
		positive_params.append("<current-temp>")
	else:
		negative_params.append("<current-temp>")
		if current_temp < 70:
			negative_params.append("<current-temp-cold>")
			add_boolean_token("<current-temp-cold?>")
		else: #current_temp > 85
			negative_params.append("<current-temp-hot>")
			add_boolean_token("<current-temp-hot?>")

	precip_inches = float(get_precip_inches())
	if precip_inches == 0:
		positive_params.append("<precip-inches>")
		positive_params.append("<precip-amount>")
	else:
		negative_params.append("<precip-inches>")
		negative_params.append("<precip-amount>")
		add_boolean_token("<is-rain?>")

	cloud_coverage_percent = int(get_cloud_coverage_percent())
	if cloud_coverage_percent <= 50:
		positive_params.append("<cloud-coverage-percent>")
		positive_params.append("<sky-description>")
		add_boolean_token("<is-clear?>")
	else:
		negative_params.append("<cloud-coverage-percent>")
		negative_params.append("<sky-description>")
		add_boolean_token("<is-overcast?>")

	'''Deciding whether humidity is negative depends on temperature.
	Thus, we created a crude formula for uncomfortability: 4000 / temp = minimum uncomfortable humidity
	(If it is only 40 degrees out, it can be 100% humid and not be bad; if it is 100 degrees, 40% is uncomfortable)'''
	humidity = int(get_humidity())
	temp = int(get_current_temp())
	if 4000 / temp >= humidity:
		positive_params.append("<humidity>")
	else:
		negative_params.append("<humidity>")
		add_boolean_token("<high-humidity?>")

	wind_speed = int(get_wind_speed())
	if wind_speed >= 20:
		add_boolean_token("<high-wind-speed?>")
	if "<current-temp-cold>" in negative_params and wind_speed > 15:
		negative_params.append("<wind-speed>")
	elif "<current-temp-hot>" in negative_params and wind_speed > 15:
		positive_params.append("<wind-speed>")

	positive_emotions_sum = int(emotion_ratios[":)"]) + int(emotion_ratios[":D"]) + int(emotion_ratios["<3"])
	negative_emotions_sum = int(emotion_ratios[":("]) + int(emotion_ratios[":'("]) + int(emotion_ratios[">:("])

	positive = positive_emotions_sum * len(positive_params)
	negative = negative_emotions_sum * len(negative_params)

	#chance to tweet neutrally if positive and negative are close
	if abs(positive-negative) <= 3:
		return choice([POSITIVE, NEGATIVE, NEUTRAL])

	if randint(1, positive + negative) <= positive:
		return POSITIVE
	else:
		return NEGATIVE

def is_boolean_param(param):
	'''A boolean_param ends with a "?>", like in "<is-rainy?>"'''
	return len(param) >= 2 and param[len(param)-2] == '?'

def tweet_neutrally_about_weather():
	return parse_tweet(choice(weather_neutral)) #TODO: stop parsing here; twitterbot will do that

def tweet_positively_about_weather():
	positive_tweets = []
	global positive_params
	global negative_params
	for param in positive_params:
		if param in weather_positive: #weather_positive maps params to positive tweets
			for tweet in weather_positive[param]:
				#don't include this tweet if it contains a negative parameter (unless it's a boolean param)
				for neg_param in negative_params:
					if tweet.find(neg_param) != -1 and not is_boolean_param(neg_param):
						break #continue outer for loop
				else:
					positive_tweets.append(tweet)
	if len(positive_tweets) == 0:
		return tweet_neutrally_about_weather()
	else:
		return parse_tweet(choice(positive_tweets)) #TODO: stop parsing here; twitterbot will do that

def tweet_negatively_about_weather():
	negative_tweets = []
	global positive_params
	global negative_params
	for param in negative_params:
		if param in weather_negative: #weather_negative maps params to negative tweets
			for tweet in weather_negative[param]:
				#don't include this tweet if it contains a positive parameter (unless it's a boolean param)
				for pos_param in positive_params:
					if tweet.find(pos_param) != -1  and not is_boolean_param(pos_param):
						break #continue outer for loop
				else:
					negative_tweets.append(tweet)
	if len(negative_tweets) == 0:
		return tweet_neutrally_about_weather()
	else:
		return parse_tweet(choice(negative_tweets)) #TODO: stop parsing here; twitterbot will do that

def tweet_about_weather():
	'''Uses all the above code to decide what to tweet about data'''
	feeling_about_weather = decide_positive_or_negative()
	if feeling_about_weather == POSITIVE:
		return tweet_positively_about_weather()
	elif feeling_about_weather == NEGATIVE:
		return tweet_negatively_about_weather()
	else:
		return tweet_neutrally_about_weather()

print(tweet_about_weather())
