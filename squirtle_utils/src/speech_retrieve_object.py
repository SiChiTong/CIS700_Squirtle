import pyttsx
import sys

if len(sys.argv)<2:
	print 'usage: python script.py [object] '
	myobject = 'stapler'
else:
	myobject = str(sys.argv[1])
print 'object: ',myobject

engine = pyttsx.init()
engine.setProperty('rate', 150)

voices = engine.getProperty('voices')
num = 16

engine.setProperty('voice', voices[num].id)

speechstring = "please give me a "+myobject
engine.say(speechstring)

engine.runAndWait()

