#!/usr/bin/env python
import roslib; roslib.load_manifest('twitterbot')
import rospy
from std_msgs.msg import String

def callback(data):
    rospy.loginfo(rospy.get_name() + ": I heard %s" % data.data)

def listener():
    rospy.init_node('twitter_processor', anonymous=False)
    rospy.Subscriber("twitter_task", String, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
