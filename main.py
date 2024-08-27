import pyttsx3
import os
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import subprocess
import sys
import google.generativeai as genai

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices[3].id)
engine.setProperty('voice', voices[1].id)
userdata = {
    'API_KEY': 'AIzaSyCE9-4Cnkr0CEvWmp7iVuGGzPpdR8_tM6Y'
}

GOOGLE_API_KEY = userdata.get('API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])
def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour <= 12:
        speak("Good Morning!")
    elif 12 <= hour <= 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your personal voice assistant. How May I help you")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        query=str(query).lower()
        if query != " " and query != "":
            response = chat.send_message(query)
            print(response.text)


    except Exception as e:
        #print(e)
        print("Say that again please...")
        return "None"
    return query

def calculate_bmi(weight, height):
    """
    Calculate the BMI using weight (in kilograms) and height (in meters).
    """
    bmi = (weight/(height * height))
    return bmi

def interpret_bmi(bmi):
    """
    Interpret the BMI value and provide a corresponding category.
    """
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal weight"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def call_emergency_services():
    # Replace '911' with your local emergency number if different
    emergency_number = "+918317097666"
    subprocess.run(["start", f"tel:{emergency_number}"], shell=True)


if __name__ == "__main__":
    wishMe()
    ai_response = None
    while True:
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=50)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        elif 'youtube' in query:
            speak("Opening Youtube...")
            webbrowser.open("https://www.youtube.com/watch?v=xrnVAbZmBCk")
        elif 'diet chart' in query:
            speak("Providing diet charts")
            webbrowser.open("https://www.planetayurveda.com/diet-chart/")
        elif "open music" in query:
            musicPath = r"C:\Users\saksh\Downloads\just-relax-11157.mp3"
            if sys.platform == "win32":
                os.startfile(musicPath)
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.Popen([opener, musicPath])
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")
        elif 'calculate bmi' in query:
            speak("Sure! Please provide your weight in kilograms.")
            weight = float(input("Enter your weight in kilograms: "))
            speak("Please provide your height in meters.")
            height = float(input("Enter your height in meters: "))
            bmi = calculate_bmi(weight, height)
            category = interpret_bmi(bmi)
            speak(f"Your BMI is {bmi:.2f}. You are categorized as {category}.")
            print(f"Your BMI is {bmi:.2f}. You are categorized as {category}.")
        elif 'first aid' in query:
            speak("Providing first aid information")
            webbrowser.open("https://www.verywellhealth.com/basic-first-aid-procedures-1298578")
        elif 'emergency' in query or 'help' in query:
            speak("Calling emergency services...")
            call_emergency_services()
        else:
            # If no command matches, send query to AI
            ai_response = chat.send_message(query).text

            # Speak out AI response
        if ai_response:
            speak(ai_response)


