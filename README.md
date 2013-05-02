bwi
===

To install this code on a computer with ROS (i.e. the robots or the lab machines):

1. Create the 'twitterbot' ROS package if it doesn't exist by running the following in Terminal:
 - roscd
 - cd class-code
 - roscreate-pkg twitterbot
2. Copy the contents of the twitterbot subdirectory of this bwi folder into the new twitterbot directory in ros (should be something like ~/ros/rosbuild_ws/class-code/twitterbot).
3. Make the python scripts executable. If you are still in the class-code directory, run:
 - cd twitterbot/scripts
 - chmod +x *.py
4. Finally, run rosmake (this step may be unnecessary):
 - rosmake twitterbot

To run our code:

1. Start ROS core:
 - roscore
2. Start the following nodes. twitterbot subscribes to the "tweet" topic and tweets messages it receives, twitter_processor subscribes to "twitter_task", queries our database, and publishes the resulting tweet to "tweet", and taskmon monitors when nodes appear and disappear on the core and publishes updates to "twitter_task".
 - rosrun twitterbot twitterbot.py
 - rosrun twitterbot twitter_processor.py
 - rosrun twitterbot taskmon.py

ROS has built-in commands to publish messages to a specific topic. For instance, to publish to the "tweet" topic (and have the robot or computer tweet on Twitter), you can run the following command:
 - rostopic pub /tweet std_msgs/String "<Text to Tweet Here>"

The Weather folder on Github is currently not used. It will eventually be used to make a weather node that publishes weather information for other people to use; right now, we just retrieve the weather and use it directly without publishing and subscribing (which is why the "weather_node.py" and "pywwo.py" are in twitterbot/scripts).

pywwo.py: a python wrapper that allows us to use the World Weather Online API in python

weather_node.py: connects to World Weather Online API to retrieve weather information

weather_processor.py: separates weather information from weather_node into positive and negative groups (ex. 75 degrees is positive, 100 is negative); based on ratio between the two and the emotion ratios of the robot, decides to tweet positively, negatively, or neutrally about the weather

taskmon.py: monitors incoming and outgoing nodes and publishes this information to "twitter-monitor"

textfile_to_database.py: converts twitter_database.txt into various structures (primarily python dictionaries) used by twitter_database.py

twitter_database.py: parses tweets with dynamic tokens into tweets with dynamic content such as emoticons, hashtags, and weather information

twitter_processor.py: subscribes to twitter_task and tweets when it hears that the robot has turned on; also tweets every 10 minutes about the weather by coordinating with the weather_processor

To run, type commands into separate terminals:
*roscore - Needed to run the next two nodes
*rosrun twitterbot twitterbot.py - subscribes to the "tweet" topic and tweets messages it receives
*rosrun twitterbot twitter_processor.py - subscribes to "twitter_task", queries our database, and publishes the resulting tweet to "tweet"; also posts weather tweets every 10 minutes
*rosrun twitterbot taskmon.py - starts the taskmon node, which monitors when nodes appear and disappear on the core; publishes "turned_on" to the twitter_task topic

The robot will initially tweet about the weather and about being turned on. It then posts about the weather every 10 minutes. Also, it seems that this doesn't often work the first time - restarting the nodes other than roscore should solve the issue.
