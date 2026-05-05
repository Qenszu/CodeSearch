import speech_recognition as sr
#from voiceRecognitionFun import activeMicrophone
from db import DB
from pprint import pprint

def voice(DB):
    r = sr.Recognizer()

    print("Initializing Speech Recognition...")

    '''
    active_microphone_list = activeMicrophone.get_active_microphones()
    print(f"Choose your device input:")
    for i, src in enumerate(active_microphone_list):
        print(f"Microphone {i}: {src}")

    ind = int(input("Select your microphone: "))

    if ind < 0 or ind >= len(active_microphone_list):
        raise ValueError("Invalid input")
    '''
    print("1. Polski\n2. English")
    lan = int(input("Select your language: "))

    match lan:
        case 1:
            lan = "pl-PL"
        case 2:
            lan = "en-EN"
        case _:
            lan = "pl-PL"

    while True:
        print("Speek now")
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

            try:
                text = r.recognize_google(audio, language=lan)
                print(text)
                if text == "exit" or text == "koniec":
                    return
                pprint(DB.query(text, 3))


            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")


