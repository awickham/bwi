#!/usr/bin/env python
import roslib; roslib.load_manifest("twitterbot")
import rospy
from std_msgs.msg import String
import twitter
import rosnode
import rosgraph
import rosgraph.masterapi
import time
from sets import Set
runningNodes = set()
pub = rospy.Publisher("twitter_task", String)

def talker():
    global pub

def talker():
    pub = rospy.Publisher("twitter_task", String)
    rospy.init_node("taskmon")
    while not rospy.is_shutdown():
        updateState()
        time.sleep(10)

def updateState():
    # Taken from rosnode source to be a little less general and more efficient
    global pub
    global runningNodes
    master = rosgraph.masterapi.Master('rosgraph', master_uri="http://128.83.122.157:11311/")
    try:
        state = master.getSystemState()
    except socket.error:
        raise ROSNodeIOException("Unable to communicate with master!")
    nodes = set()
    for s in state: # one of publishers, subscribers, or services
        for t, l in s: # topics and participants of topics
            for node in l:
                if not node in runningNodes:
                    pub.publish("new node %s appeared" % node)
                    if node == "segbot_gazebo":
                        pub.publish("turned_on")
                    runningNodes.add(node)
    nodesToRemove = []
    for node in runningNodes:
        if not node in nodes:
            pub.publish("old node %s vanished" % node)
            if node == "segbot_gazebo":
                pub.publish("turned_off")
            nodesToRemove.append(node)
    for node in nodesToRemove:
        runningNodes.remove(node)


if __name__ == "__main__":
    talker()
