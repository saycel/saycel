from IPython import embed
import pyowm
import subprocess


owm = pyowm.OWM('db1195d9a23fe8e7fb99acb4370025c9')  # You MUST provide a valid API key

fc = owm.daily_forecast('Pearl Lagoon, ni', limit=6)
todays_weather = fc.get_forecast().get_weathers()[0]
morning_temp = todays_weather.get_temperature(unit='celsius')['morn']
eve_temp = todays_weather.get_temperature(unit='celsius')['eve']
day_temp = todays_weather.get_temperature(unit='celsius')['day']

max_temp = todays_weather.get_temperature(unit='celsius')['max']
min_temp = todays_weather.get_temperature(unit='celsius')['min']
sunset = todays_weather.get_sunset_time("iso")
detailed_status = todays_weather.get_detailed_status()
humidity = todays_weather.get_humidity()


text = "Good Morning Pearl Lagoon. "
text += "This morning it will be " + str(morning_temp) + " celsius. Later in the day it will be " + str(day_temp) +" celsius. "
text += "There will be " + str(detailed_status) + ". "


embed() 


subprocess.call([
    "curl",
    "--data",
    "text="+text+"&btype=all", 
    "http://127.0.0.1:8085/sms/send_broadcast"
])


