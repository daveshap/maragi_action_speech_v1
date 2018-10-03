import pyttsx3


engine = pyttsx3.init()
while True:
    a = input('what do you want me to say?   ')
    engine.say(a)
    engine.runAndWait()