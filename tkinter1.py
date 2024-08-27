import pyttsx3
import os
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import subprocess
import sys
import google.generativeai as genai
import tkinter as tk

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

userdata = {
    'API_KEY': 'your api key'
}

GOOGLE_API_KEY = userdata.get('API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])


def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    response_text.config(state=tk.NORMAL)
    response_text.delete(1.0, tk.END)  # Clear the previous response
    response_text.insert(tk.END, audio + '\n')
    response_text.config(state=tk.DISABLED)
    response_text.see(tk.END)


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
        query = ""
        languages = ['en-in', 'hi-IN', 'ur-PK', 'de-DE', 'fr-FR']
        for lang in languages:
            try:
                query = r.recognize_google(audio, language=lang)
                print(f"User said in {lang}: {query}\n")
                break
            except sr.UnknownValueError:
                print(f"Speech not understood in {lang}")
            except sr.RequestError as e:
                print(f"Could not request results for {lang}; {e}")
        return query.lower()
    except Exception as e:
        print("Say that again please...")
        return ""


def call_emergency_services():
    emergency_number = "+918355007336"
    subprocess.run(["start", f"tel:{emergency_number}"], shell=True)


def provide_diet_recommendations(user_info, disease):
    # Query OpenAI API to generate diet recommendations for the given disease
    ai_response = chat.send_message(f"Diet recommendations for {disease}").text

    # Split the response into sentences
    sentences = ai_response.split('. ')

    # Select the first five sentences
    selected_sentences = '. '.join(sentences[:5])

    # Present recommendations to the user
    speak("Here are your personalized diet recommendations for managing " + disease + ":")
    speak(selected_sentences)
    print(selected_sentences)


def get_user_info():
    speak("Please tell me your weight in kilograms.")
    weight = float(input("Enter your weight in kilograms: "))
    speak("Please tell me your height in meters.")
    height = float(input("Enter your height in meters: "))

    return {'weight': weight, 'height': height}


def nutrition_and_diet_management(query):
    if 'Diet chart' in query:
        speak("Providing diet charts")
        webbrowser.open("https://www.planetayurveda.com/diet-chart/")
    elif 'Informations' in query:
        user_info = get_user_info()
        speak("Sure, please tell me which disease you want to manage through diet?")
        disease = takeCommand()
        provide_diet_recommendations(user_info, disease)
    else:
        speak("Sorry, I didn't understand that command.")

def calculate_bmi_function():
    speak("Sure! Please provide your weight in kilograms.")
    weight = float(input("Enter your weight in kilograms: "))
    speak("Please provide your height in meters.")
    height = float(input("Enter your height in meters: "))
    bmi = weight / (height ** 2)
    speak(f"Your BMI is {bmi:.2f}.")



def on_submit():
    query = input_entry.get()
    input_entry.delete(0, tk.END)

    if 'wikipedia' in query:
        speak("Searching Wikipedia...")
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=5)
        speak("According to Wikipedia")
        speak(results)

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
        speak(f"Your BMI is {bmi:.2f}. You are categorized as {category}.")
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

def listen():
    query = takeCommand()
    if query:
        input_entry.delete(0, tk.END)
        input_entry.insert(tk.END, query)
        on_submit()

def stop_listening():
    global listening
    listening = False
    engine.stop()

root = tk.Tk()
input_label = tk.Label(root, text="Text Input:", font=("Arial", 14))
input_label.grid(row=0, column=1, padx=(1, 0), pady=(10, 5))  # Adjusted padx value to (5, 5)
input_entry = tk.Entry(root, width=45, font=("Arial", 12))
input_entry.grid(row=0, column=2, padx=(0, 1), pady=(10, 5))  # Adjusted padx value to (0, 5)

# Dropdown menu
options = ["Wikipedia", "YouTube", "Time", "Calculate BMI", "First Aid", "Diet chart", "Informations"]
selected_option = tk.StringVar(root)
selected_option.set(options[0])  # Default value
select_menu = tk.Menubutton(root, indicatoron=True, direction="below", width=0, height=0)
select_menu.menu = tk.Menu(select_menu, tearoff=False)
select_menu["menu"] = select_menu.menu
for option in options:
    select_menu.menu.add_command(label=option)
select_menu.grid(row=0, column=3, padx=1, pady=20)

listen_button = tk.Button(root, text="Speak", command=listen, width=15, height=2)
listen_button.grid(row=1, column=2, padx=5, pady=1)


# BMI button
bmi_button = tk.Button(root, text="Calculate BMI", command=calculate_bmi_function, width=15, height=2)
bmi_button.grid(row=2, column=1, padx=(10, 0), pady=20)

# emergency button
emergency_button = tk.Button(root, text="Emergency", command=call_emergency_services, width=15, height=2)
emergency_button.grid(row=2, column=3, padx=(0, 10), pady=20)


# Text box for response
response_label = tk.Label(root, text="Response:", font=("Arial", 14))
response_label.grid(row=3, column=1, padx=(10, 0), pady=10)
response_text = tk.Text(root, width=50, height=10, state='normal')
response_text.grid(row=3, column=2, columnspan=3, padx=(0, 10), pady=10)

# Submit button
submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.grid(row=4, column=1, padx=(200, 1), pady=5)  # Adjust padx for Submit button

# Stop button
stop_button = tk.Button(root, text="Stop", command=stop_listening)
stop_button.grid(row=4, column=2, padx=(1, 200), pady=5)  # Adjust padx for Stop button


listening = False
wishMe()  # Call the wishMe function to greet the user when the GUI is launched

root.mainloop()
