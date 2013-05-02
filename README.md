bwi
===

Authors: Andy Wickham, Tony Wickham, and Ryan Zabcik

Contact us at: {awickham, tonyw, ryanz}@cs.utexas.edu



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
2. Start the following nodes in separate Terminal windows. twitterbot subscribes to the "tweet" topic and tweets messages it receives, twitter_processor subscribes to "twitter_task", queries our database, and publishes the resulting tweet to "tweet", and taskmon monitors when nodes appear and disappear on the core and publishes updates to "twitter_task".
 - rosrun twitterbot twitterbot.py
 - rosrun twitterbot twitter_processor.py
 - rosrun twitterbot taskmon.py
3. ROS has built-in commands to publish messages to a specific topic. For instance, to publish to the "tweet" topic (and have the robot or computer tweet on Twitter), you can run the following command in a 5th Terminal window:
 - rostopic pub /tweet std_msgs/String "<Text to Tweet Here>"

To attach a Twitter account to a new robot:

1. Create the Twitter account with the following credentials:
 - Full name: the name of the robot (i.e. "Bender").
 - Email: bwitwitter@gmail.com
 - Password: We have a secure password generator that we have used for the current accounts, but you can use any memorable password you like.
2. Select a username. Our username format is "gdc_" followed by the robot's name (i.e. "gdc_bender"). 
3. Sign in with this new account at dev.twitter.com.
4. Hover over your image in the top right corner and click "My applications".
5. Click on the button that says "Create a new application".
6. Fill in the following details:
 - Name: same as username (i.e. "gdc_bender")
 - Description: Whatever you like; we've said something like "Posts updates about what the BWI robots are doing"
 - Website: We've linked to our Wiki page at http://zweb.cs.utexas.edu/users/piyushk/bwi/index.php/CS378/Robot_Personality
7. Agree to the Terms and Conditions, fill out the CAPTCHA, and finalize by clicking the button at the bottom.
8. Click on the "Create my access token" button on the bottom of the following page.
9. While that processes, click on the "Settings" tab, scroll down, and change the access mode (under "Application Type") to "Read, Write and Access direct messages".
10. Now we need to put these credentials in our twitterbot node. We would like this to be more secure, but for now these are essentially plain text in the code.
 - Navigate to ~/ros/rosbuild_ws/class-code/twitterbot/scripts
 - Open twitterbot.py (to edit, not to run)
 - Follow the outline of the credentials listed to add those for the new account. They are on the dev.twitter.com page that you should still have open (under the "Details" tab).
 - In the getApi function, add an elif statement following the pattern of the existing elif statements (before the final else). Note that compName should be the name of the robot in lowercase.
 - You should be set! Now when the twitterbot node is running on the new robot, it should tweet to its Twitter account when it hears a message on the "tweet" topic.

To update the database used to generate tweets:

1. Navigate to ~/ros/rosbuild_ws/class-code/twitterbot/scripts
2. Open twitter_database.txt.
3. Add relevant words or tweet structures under the various subsections, using the comments for guidance.
4. Push changes to GitHub (the twitter_processor and weather_processor nodes use textfile_to_database.py to download the database from there so we can update it dynamically from any computer).
 - Note that you will need to contact us to get permission to push to our GitHub repository. You can do this using our emails at the top of this README.

To have the robots tweet about a new node:

1. Navigate to ~/ros/rosbuild_ws/class-code/twitterbot/scripts
2. Open taskmon.py (to edit, not to run).
3. In the updateState function, there is a triply-nested 'for' loop containing an 'if' statement. There you will see the following 'if' statement (possibly followed by other similar statements):
 if node == "/segway_rmp_node":
         pub.publish("turned_on")
4. Add an 'elif node == "/<YOUR_NODE_NAME_HERE>":' statement, followed by 'pub.publish("<SOME_RELEVANT_STATE_NAME">'
5. If you want to tweet when your node ends, you can also add a similar statement nearer to the bottom underneath 'pub.publish("turned_off")'. The published message cannot be the same as any other published messages (including the message you sent when the node started).
6. Save and exit, and open twitter_database.txt.
7. At the bottom you will see a section labeled TWEET DICTIONARY with various Keys and other text.
8. Add 'Key = <YOUR_RELEVANT_STATE_NAME>' followed by possible phrases to tweet when your node starts/ends (one will be picked at random). Note that these phrases can (and should) include dynamic tokens.



Quick Reference Guide and Notes:

 - The Weather folder on Github is currently not used. It will eventually be used to make a weather node that publishes weather information for other people to use; right now, we just retrieve the weather and use it directly without publishing and subscribing (which is why the "weather_node.py" and "pywwo.py" are in twitterbot/scripts).
 - pywwo.py is a python wrapper that allows us to use the World Weather Online API in python
 - weather_node.py: connects to World Weather Online API to retrieve weather information
 - weather_processor.py separates weather information from weather_node into positive and negative groups (i.e. 75 degrees is positive, 100 is negative [too hot]); based on ratio of these groups and the emotion ratios of the robot, it decides to tweet positively, negatively, or neutrally about the weather
 - taskmon.py: monitors when other ROS nodes start and end and publishes this information to "twitter_task"
 - twitter_processor.py: subscribes to "twitter_task" and tweets (by publishing to "tweet") when it hears that the robot has turned on; also tweets every 10 minutes about the weather by coordinating with the weather_processor
 - textfile_to_database.py: converts twitter_database.txt (downloaded from GitHub at runtime) into various structures (primarily python dictionaries) used by twitter_database.py
 - twitter_database.py: parses tweets with dynamic tokens into tweets with dynamic content such as emoticons, hashtags, and weather information

The robot will initially tweet about the weather and about being turned on. It then posts about the weather every 10 minutes. Also, it seems that this doesn't often work the first time - restarting the nodes other than roscore should solve the issue.
