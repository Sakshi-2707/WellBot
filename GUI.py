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
        return query.lower()
    except Exception as e:
        print("Say that again please...")
        return ""


def call_emergency_services():
    emergency_number = "+918355007336"
    subprocess.run(["start", f"tel:{emergency_number}"], shell=True)


def provide_diet_recommendations(user_info, disease):

    ai_response = chat.send_message(f"Diet recommendations for {disease}").text

    # Present recommendations to the user
    speak("Here are your personalized diet recommendations for managing " + disease + ":")
    speak(ai_response)

    with open("diet_recommendations.txt", "a") as file:
        file.write(f"Diet recommendations for {disease}:\n")
        file.write(ai_response + "\n")
    print(ai_response)


def get_user_info():
    speak("Please tell me your weight in kilograms.")
    weight = float(input("Enter your weight in kilograms: "))
    speak("Please tell me your height in meters.")
    height = float(input("Enter your height in meters: "))

    return {'weight': weight, 'height': height}


def nutrition_and_diet_management(query):
    if 'diet chart' in query:
        speak("Providing diet charts")
        webbrowser.open("https://www.planetayurveda.com/diet-chart/")
    elif 'nutrition' in query or 'diet' in query:
        user_info = get_user_info()
        speak("Sure, please tell me which disease you want to manage through diet?")
        disease = takeCommand()
        provide_diet_recommendations(user_info, disease)
    else:
        speak("Sorry, I didn't understand that command.")


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
        elif 'youtube' in query:
            speak("Opening Youtube...")
            webbrowser.open("https://www.youtube.com/watch?v=xrnVAbZmBCk")
        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")
        elif 'calculate bmi' in query:
            speak("Sure! Please provide your weight in kilograms.")
            weight = float(input("Enter your weight in kilograms: "))
            speak("Please provide your height in meters.")
            height = float(input("Enter your height in meters: "))
            bmi = calculate_bmi(weight, height)
            category = interpret_bmi(bmi)
            speak(f"Your BMI is {bmi:.2f}. You is {bmi:.2f}. You are categorized as {category}.")
            print(f"Your BMI is {bmi:.2f}. You are categorized as {category}.")
        elif 'first aid' in query:
            speak("Providing first aid information")
            webbrowser.open("https://www.verywellhealth.com/basic-first-aid-procedures-1298578")
        elif 'emergency' in query or 'help' in query:
            speak("Calling emergency services...")
            call_emergency_services()
        else:
            # Handle nutrition and diet management related queries
            nutrition_and_diet_management(query)
