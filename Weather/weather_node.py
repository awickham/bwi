from pywwo import *

setKey('h6zcfapfu9647c285nyzdgvb', 'free')
w=LocalWeather('Austin, TX, United States')

#Current weather
current_temp = w.data.current_condition.temp_F
curr_precipMM = w.data.current_condition.precipMM
humidity = w.data.current_condition.humidity
cloudcover = w.data.current_condition.cloudcover
curr_weatherDesc = w.data.current_condition.weatherDesc

#Forecasted weather
high = w.data.weather.tempMaxF
low = w.data.weather.tempMinF
forecasted_precipMM = w.data.weather.precipMM
forecasted_weatherDesc = w.data.weather.weatherDesc

print "Today's Forecast"
print "High: %s degrees Fahrenheit" % (high)
print "Low: %s degrees Fahrenheit" % (low)
print "Precipitation prediction: %s milimeters" % (str(forecasted_precipMM))
print "Weather description: %s" % (forecasted_weatherDesc)
print ""
print "Current weather"
print "Temperature: %s degrees Fahrenheit" % (current_temp)
print "Precipitation: %s milimeters" % (str(curr_precipMM))
print "Humidity: %s percent" % (str(humidity))
print "Cloud coverage: %s percent" % (str(cloudcover))
print "Weather description: %s" % (curr_weatherDesc)
