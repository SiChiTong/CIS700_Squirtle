import pyttsx
import sys

if len(sys.argv)<3:
	print 'usage: python script.py [object] [location]'
	myobject = 'stapler'
	location = 'desk'
else:
	myobject = str(sys.argv[1])
	location = str(sys.argv[2])
print 'object: ',myobject,', location: ',location

engine = pyttsx.init()
engine.setProperty('rate', 150)

voices = engine.getProperty('voices')
num = 16

engine.setProperty('voice', voices[num].id)

speechstring = "please place my "+myobject+" on or near the "+location # +". And press the button." 
engine.say(speechstring)

engine.runAndWait()

