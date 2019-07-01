import time
import speech_recognition as sr
import os
from time import ctime
from playsound import playsound
import pyowm
import json
from subprocess import call

owm = pyowm.OWM('a7c502158f1ab652bb2ac41c6de4bc9f')
observation = owm.weather_at_place('Athens,GR')

def say(txt):
	call(["C:\Program Files (x86)\eSpeak\command_line\espeak", txt])
'''
def recordAudio():
    # Record Audio
    r = sr.Recognizer()
	r.pause_threshold = 0.2
	r.phrase_threshold = 0.2
	r.non_speaking_duration = 0.1
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
 
    # Speech recognition using Google Speech Recognition
    data = ""
    try:
        # Uses the default API key
        # To use another API key: `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        data = r.recognize_google(audio)
        print("You said: " + data)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
 
    return data
'''

while True:
	# Record Audio
	r = sr.Recognizer()
	r.pause_threshold = 0.2
	r.phrase_threshold = 0.2
	r.non_speaking_duration = 0.1
	with sr.Microphone() as source:
		print("Listening...")
		audio = r.listen(source)
		data = ""
		try:
			data = r.recognize_google(audio)
			print(">>> " + data)
			if "Alex" in data:
				playsound('Siri1.mp3')
				r.pause_threshold = 0.8
				r.phrase_threshold = 0.4
				r.non_speaking_duration = 0.3
				with sr.Microphone() as source:
					print("Say something!")
					audio = r.listen(source)
				data = ""
				try:
					data = r.recognize_google(audio)
					print("You said: " + data)
					if "weather" in data:
						w = observation.get_weather()
						text1 = str(w)
						text2 = text1.replace("<", '{"ver": "')
						text3 = text2.replace(", ", '", "')
						text4 = text3.replace("=", '":"')
						text5 = text4.replace('":"', "=", 1)
						text6 = text5.replace(">", '"}')
						weather_now = json.loads(str(text6))
						
						wind1 = w.get_wind()
						wind2 = str(wind1)
						wind3 = wind2.replace("'", '"')
						wind = json.loads(wind3)
						
						humidity = w.get_humidity()
						
						temperature1 = w.get_temperature('celsius')
						temperature2 = str(temperature1)
						temperature3 = temperature2.replace("'", '"')
						temperature4 = temperature3.replace(": ", ': "')
						temperature5 = temperature4.replace(", ", '", ')
						temperature6 = temperature5.replace("}", '"}')
						temperature = json.loads(str(temperature6))

						
						weather_forcast = ("Weather now: In the sky we have", weather_now['status'], "the wind speed is:", wind['speed'], "kilometers per hour, humidity is at:", humidity, "and the temperature is:", temperature['temp'], "degrees Celsius.")
						print(weather_forcast)
						say(str(weather_forcast))
				except sr.UnknownValueError:
					print("Google Speech Recognition could not understand audio or Lost focus")
				except sr.RequestError as e:
					print("Could not request results from Google Speech Recognition service; {0}".format(e))
		except sr.UnknownValueError:
			print(">>> Incomprehensible")#print("Google Speech Recognition could not understand audio")
		except sr.RequestError as e:
			print("Could not request results from Google Speech Recognition service; {0}".format(e))
