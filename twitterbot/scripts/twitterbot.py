#!/usr/bin/env python
import roslib; roslib.load_manifest('twitterbot')
import rospy
from std_msgs.msg import String
import twitter
import platform #to check computer name

#credentials
ebooks_consumer_key = 'B9mwrhOkQ65oE50JrEuw'
ebooks_consumer_secret = '607fnxIrc0dpOAx0jfxk53ac0VaH03mHzIMcuOaCddI'
ebooks_access_token = '1244870965-ExsbSasa6wxROZ5DgHFVJTy33GxG25hPBgDhIE'
ebooks_access_token_secret = '9mEtUX5c6NhC0ZSbxQFxKHduYnRJfS5zq36aCijN54'

marvin_consumer_key = 'mkMJbXaja0Qi2BJqG555iw'
marvin_consumer_secret = 'W9lJolkTimxXUtENpYymJNAez7Tw6DFqMf1K71XlX4'
marvin_access_token = '1244844690-SdBJz4lyo47C0k2gAN94wWihaskGCO6A9bJb5Xm'
marvin_access_token_secret = 'HPo0KtKgDIvNBuR2vHGjBIG1ShqOGaFxRvNpg9YF4'

bender_consumer_key = '2joSTjEbkN1V7LOgoEey3w'
bender_consumer_secret = 'Mp7aDJHctQOhGzsscguLJl2UvOF5QdaEnKgKEy0'
bender_access_token = '1244852696-CpOXSTl2FRn7zoubPtfTHnWXYJ5LO807vEdhZJy'
bender_access_token_secret = 'HaqRSnPN4b7BoNvkeX9ZU1IkCaulcE4GCFZF5nySus'

clamps_consumer_key = 'LXJh6f2VHO2ohJ1RLgJW1g'
clamps_consumer_secret = 'jOpNt4rfmVo0InowmR0o5dWQBeXNmO8HLd8wiaCesI'
clamps_access_token = '1244858930-Z3e9uUCy8CNJ8H3EJX24gP7rulcPDALPDGfNSda'
clamps_access_token_secret = '3aSlH9xsQTedJFqkBYZpKFNc1Qe8xueJlD0D6qHIuI'

calculon_consumer_key = 'aiAqKeLXIsYOngINOy8g'
calculon_consumer_secret = 'Wnf2bRwo3JrViHaVvOpqY5TCxp0eZWB3GsDEK8TYR5o'
calculon_access_token = '1244839182-FUE7QlVi4fnBG0pIVU1yRVOKznKnugZ4s76p6f2'
calculon_access_token_secret = '92X6OUAvbureRinH0sfV3hxjREiYxEsftUSd1QZYY4'

api = None

def getApi(compName):
    if compName == 'marvin':
        return twitter.Api(marvin_consumer_key,
		marvin_consumer_secret,
		marvin_access_token,
		marvin_access_token_secret)
    elif compName == 'bender':
        return twitter.Api(bender_consumer_key,
		bender_consumer_secret,
		bender_access_token,
		bender_access_token_secret)
    elif compName == 'clamps':
        return twitter.Api(clamps_consumer_key,
		clamps_consumer_secret,
		clamps_access_token,
		clamps_access_token_secret)
    elif compName == 'calculon':
        return twitter.Api(calculon_consumer_key,
                calculon_consumer_secret,
                calculon_access_token,
                calculon_access_token_secret)
    else: #use test account if not on one of the robots
        return twitter.Api(ebooks_consumer_key,
		ebooks_consumer_secret,
		ebooks_access_token,
		ebooks_access_token_secret)

def callback(message):
    #splits the message into multiple tweets if > 140 characters
    api.PostUpdates(message.data)
    rospy.loginfo("Tweeted the following message(s): %s", message.data)

def listener():
    rospy.init_node('twitterbot', anonymous=False)
    rospy.Subscriber("tweet", String, callback)
    rospy.spin()


if __name__ == '__main__':
    computerName = platform.node()
    api = getApi(computerName)
    listener()
