#!/usr/bin/env python
import roslib; roslib.load_manifest('twitterbot')
import rospy
from std_msgs.msg import String

tweet_history = []
time_of_last_tweet = 0.0
twitter_task = ""
DOWN_TIME = 600 # in seconds


def pub_tweet():
    # update global variables
    global twitter_task
    # figure out what to tweet
    tweet = twitter_task # TODO
    global tweet_history
    tweet_history.append(tweet)
    global time_of_last_tweet
    time_of_last_tweet = rospy.get_time()

    # tweet the tweet
    pub = rospy.Publisher('tweet', String)
    rospy.init_node('twitter_processor')
    rospy.loginfo(tweet)
    pub.publish(String(tweet))

def callback(data):
    global time_of_last_tweet
    global twitter_task
    twitter_task = data.data
    rospy.loginfo(rospy.get_name() + ": I heard %s" % twitter_task)
    # determine if we should post another tweet
    if rospy.get_time() - time_of_last_tweet >= DOWN_TIME:
	try:
            pub_tweet()
        except rospy.ROSInterruptException:
            pass

def listener():
    rospy.init_node('twitter_processor', anonymous=False)
    rospy.Subscriber("twitter_task", String, callback)

    # initialize global variables
    global time_of_last_tweet
    time_of_last_tweet = rospy.get_time()

    rospy.spin()

if __name__ == '__main__':
    # start listening for twitter_task
    listener()
