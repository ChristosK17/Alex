from __future__ import print_function
import time
import speech_recognition as sr
import os
from time import ctime
from playsound import playsound
import pyowm
import json
from subprocess import call
import webbrowser
import serial
from yeelight import Bulb
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

owm = pyowm.OWM('a7c502158f1ab652bb2ac41c6de4bc9f')
observation = owm.weather_at_place('Athens,GR')

#ser = serial.Serial('COM4', 9600)

bulb = Bulb("192.168.1.9")

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'

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
def getEvents(num):
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now, maxResults=int(num), singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

while True:
	# Record Audio
	#r = sr.Recognizer()
	#r.pause_threshold = 0.2
	#r.phrase_threshold = 0.2
	#r.non_speaking_duration = 0.1
	with sr.Microphone() as source:
		#print("Listening...")
		#audio = r.listen(source)
		data = ""
		try:
			data = input("Say something: ")#input("Say something: ")#
			print(">>> " + data)
			if "Alex" in data:
				playsound('Siri1.mp3')
				#r.pause_threshold = 0.8
				#r.phrase_threshold = 0.4
				#r.non_speaking_duration = 0.3
				with sr.Microphone() as source:
					print("Say something!")
					#audio = r.listen(source)
				data = ""
				try:
					data = input("Say something: ")#r.recognize_google(audio)#
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

						
						weather_forcast = ("Weather now: In the sky we have", weather_now['status'], "the wind speed is:", wind['speed'], "kilometers per hour, humidity is at:", humidity, "and the temperature is:", temperature['temp'], "degrees Celsius")
						print(weather_forcast)
						say(str(weather_forcast))
						
					if "open" in data or "turn on" in data or "enable" in data:
						if ("light" or "lights") in data:
							if "bed" in data:
								print("Opening bed light")
								ser.write(b'B')
							if "desk" in data:
								print("Opening desk light")
								ser.write(b'D')
							if "main" in data:
								print("Opening main light")
								bulb.turn_on()
							if "all" in data:
								print("Opening all lights")
								ser.write(b'A')

					if "close" in data or "turn off" in data or "disable" in data:
						if ("light" or "lights") in data:
							if "bed" in data:
								print("Closing bed light")
								ser.write(b'b')
							if "desk" in data:
								print("Closing desk light")
								ser.write(b'd')
							if "main" in data:
								print("Closing main light")
								bulb.turn_off()
							if "all" in data:
								print("Closing all lights")
								ser.write(b'a')
								
					if "play" in data:
						print("Playing: ", data[5:])
						url = "https://www.youtube.com/results?search_query="+str(data[5:]).replace(" ","+")
						webbrowser.open(url)
						
					if "potato" in data:
						bulb.turn_off()
						time.sleep(1)
						bulb.turn_on(effect="smooth", duration=3000)
						bulb.set_rgb(255, 40, 166)
						bulb.set_hsv(324, 88, 100)
						bulb.set_brightness(10)
						bulb.turn_on(effect="smooth", duration=3000)
						url = "https://www.youtube.com/watch?v=_DjE4gbIVZk&list=PL40O1IfpNPSruc6OIDWP95BTCGTd6tZQC&index=2&t=0s"
						webbrowser.open(url)
						
					if "to do" or "tasks for" in data:
						if ("today" or "this day") in data:
							getEvents(1)
						if ("tomorrow" or "next day") in data:
							getEvents(2)
						if "week" in data:
							getEvents(10)

				except sr.UnknownValueError:
					print("Google Speech Recognition could not understand audio or Lost focus")
				except sr.RequestError as e:
					print("Could not request results from Google Speech Recognition service; {0}".format(e))
		except sr.UnknownValueError:
			print(">>> Incomprehensible")#print("Google Speech Recognition could not understand audio")
		except sr.RequestError as e:
			print("Could not request results from Google Speech Recognition service; {0}".format(e))
