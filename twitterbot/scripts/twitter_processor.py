#!/usr/bin/env python
import roslib; roslib.load_manifest('twitterbot')
import rospy
from std_msgs.msg import String

from twitter_database import *
import weather_processor
from random import choice

tweet_history = []
time_of_last_tweet = 0.0
twitter_task = ""
DOWN_TIME = 0 # in seconds

'''Constant tweet_types'''
TWEET_DICTIONARY = 0
WEATHER = 1

def pub_tweet(tweet_type):
	# update global variables
	global twitter_task

	# figure out what to tweet
	tweet = ""
	if tweet_type == TWEET_DICTIONARY:
		tweet = choice(tweet_dictionary[twitter_task])
	elif tweet_type == WEATHER:
		tweet = weather_processor.tweet_about_weather()
	else:
		tweet = "Internal problem... I hope someone fixes me soon!"

	#update history
	global tweet_history
	tweet_history.append(tweet)
	global time_of_last_tweet
	time_of_last_tweet = rospy.get_time()

	# tweet the tweet
	pub = rospy.Publisher("tweet", String, latch=True)
	pub.publish(tweet)
	rospy.loginfo("Sent following string to be tweeted: " + tweet)

def callback(data):
	global time_of_last_tweet
	global twitter_task
	twitter_task = data.data
	rospy.loginfo(rospy.get_name() + ": I heard %s" % twitter_task)
	# determine if we should post another tweet
	if rospy.get_time() - time_of_last_tweet >= DOWN_TIME:
		try:
			pub_tweet(TWEET_DICTIONARY)
		except rospy.ROSInterruptException:
			pass

def listener():
	rospy.init_node('twitter_processor', anonymous=False)
	rospy.Subscriber("twitter_task", String, callback)

	# initialize global variables
	global time_of_last_tweet
	time_of_last_tweet = rospy.get_time()

	# start publishing weather tweets
	while not rospy.is_shutdown():
		weather_tweet()

	rospy.spin()

import time
def weather_tweet():
	pub_tweet(WEATHER)
	time.sleep(14400) #four hours

if __name__ == '__main__':
	# start listening for twitter_task
	listener()
