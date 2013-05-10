from pywwo import *

setKey('h6zcfapfu9647c285nyzdgvb', 'free')
ZIP_CODE = str(78712)
w=LocalWeather(ZIP_CODE)

inches_per_milimeter = 0.039370

#Current weather
def current_temp():
	w=LocalWeather(ZIP_CODE)
    return w.data.current_condition.temp_F
def curr_precip_inches():
	w=LocalWeather(ZIP_CODE)
    return w.data.current_condition.precipMM * inches_per_milimeter
def humidity():
	w=LocalWeather(ZIP_CODE)
    return w.data.current_condition.humidity
def cloudcover():
	w=LocalWeather(ZIP_CODE)
    return w.data.current_condition.cloudcover
def windSpeed():
	w=LocalWeather(ZIP_CODE)
	return w.data.current_condition.windspeedMiles
def curr_weatherDesc():
	w=LocalWeather(ZIP_CODE)
    return w.data.current_condition.weatherDesc
def observation_time():
	'''Returns observed hour (1-24)'''
	w=LocalWeather(ZIP_CODE)
	time = str(w.data.current_condition.observation_time)
	h = int(time[:2])
	m = int(time[3:5])
	if time[6:] == 'PM':
		h += 12
	return h - 5 #from UTC to Central Time

#Forecasted weather
high = LocalWeather(ZIP_CODE).data.weather.tempMaxF
low = LocalWeather(ZIP_CODE).data.weather.tempMinF
forecasted_precip_inches = LocalWeather(ZIP_CODE).data.weather.precipMM * inches_per_milimeter
forecasted_weatherDesc = LocalWeather(ZIP_CODE).data.weather.weatherDesc

'''
print "Today's Forecast"
print "High: %s degrees Fahrenheit" % (high)
print "Low: %s degrees Fahrenheit" % (low)
print "Precipitation prediction: %s inches" % (str(forecasted_precip_inches))
print "Weather description: %s" % (forecasted_weatherDesc)
print ""
print "Current weather"
print "Temperature: %s degrees Fahrenheit" % (current_temp)
print "Precipitation: %s inches" % (str(curr_precip_inches))
print "Humidity: %s percent" % (str(humidity))
print "Cloud coverage: %s percent" % (str(cloudcover))
print "Weather description: %s" % (curr_weatherDesc)
'''
