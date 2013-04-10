import roslib; roslib.load_manifest('twitterbot')
import rospy
from std_msgs.msg import String
import twitter
import rosnode
import rosgraph

from sets import Set
Set runningNodes = Set([])

def talker():
    pub = rospy.Publisher('taskmon_talker', String)
    rospy.init_node('taskmon')
    while not rospy.is_shutdown():
        newRunningNodes = Set(rosnode.get_node_names())
        for newnode in newRunningNodes:
            if newnode not in runningNodes:
                pub.publish


def updateState():
    """Taken from rosnode source to be a little less general and more efficient"""
    master = rosgraph.master('/rosnode')
    try:
        state = master.getSystemState()
    except socket.error:
        raise ROSNodeIOException("Unable to communicate with master!")
    nodes = Set([])
    for s in state: # one of publishers, subscribers, or services
        for t, l in s: # topics and participants of topics

            


if __name__ == '__main__':
    talker()
