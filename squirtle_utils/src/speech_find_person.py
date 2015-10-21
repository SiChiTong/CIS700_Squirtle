import pyttsx
import sys

if len(sys.argv)<2:
	print 'usage: python script.py [person] '
	person = 'David'
else:
	person = str(sys.argv[1])
print 'Name: ',person

engine = pyttsx.init()
engine.setProperty('rate', 150)

voices = engine.getProperty('voices')
num = 16

engine.setProperty('voice', voices[num].id)

speechstring = "Hey, "+person+"! Come over here."
engine.say(speechstring)

engine.runAndWait()

