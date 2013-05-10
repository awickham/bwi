from pywwo import *

setKey('h6zcfapfu9647c285nyzdgvb', 'free')
ZIP_CODE = "78712"

inches_per_milimeter = 0.039370

#Forecasted weather
high = LocalWeather(ZIP_CODE).data.weather.tempMaxF
low = LocalWeather(ZIP_CODE).data.weather.tempMinF
forecasted_precip_inches = LocalWeather(ZIP_CODE).data.weather.precipMM * inches_per_milimeter
forecasted_weatherDesc = LocalWeather(ZIP_CODE).data.weather.weatherDesc

#Current weather
current_temp = LocalWeather(ZIP_CODE).data.current_condition.temp_F
curr_precip_inches = LocalWeather(ZIP_CODE).data.current_condition.precipMM * inches_per_milimeter
humidity = LocalWeather(ZIP_CODE).data.current_condition.humidity
cloudcover = LocalWeather(ZIP_CODE).data.current_condition.cloudcover
windSpeed = LocalWeather(ZIP_CODE).data.current_condition.windspeedMiles
curr_weatherDesc = LocalWeather(ZIP_CODE).data.current_condition.weatherDesc

def observation_time():
	'''Returns observed hour (1-24)'''
	w=LocalWeather(ZIP_CODE)
	time = str(w.data.current_condition.observation_time)
	h = int(time[:2])
	m = int(time[3:5])
	if time[6:] == 'PM':
		h += 12
	return h - 5 #from UTC to Central Time

'''
print "Today's Forecast"
print "High: %s degrees Fahrenheit" % (high)
print "Low: %s degrees Fahrenheit" % (low)
print "Precipitation prediction: %s inches" % (str(forecasted_precip_inches))
print "Weather description: %s" % (forecasted_weatherDesc)
print ""
print "Current weather"
print "Temperature: %s degrees Fahrenheit" % (current_temp())
print "Precipitation: %s inches" % (str(curr_precip_inches()))
print "Humidity: %s percent" % (str(humidity()))
print "Cloud coverage: %s percent" % (str(cloudcover()))
print "Weather description: %s" % (curr_weatherDesc())
'''
