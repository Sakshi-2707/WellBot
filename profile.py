import tkinter as tk
from tkinter import ttk
import pyttsx3
import os
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import google.generativeai as genai
import random
import subprocess
import sys
import platform

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
    response_text.config(state=tk.NORMAL)
    response_text.delete(1.0, tk.END)  # Clear the previous response
    response_text.insert(tk.END, audio + '\n')
    response_text.config(state=tk.DISABLED)
    response_text.see(tk.END)

def greet_user():
    send_motivational_message()

# Function to generate a motivational message
def get_motivational_message():
    messages = [
        "Believe you can and you're halfway there. - Theodore Roosevelt",
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
        "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
        "Your limitation—it's only your imagination.",
        "Push yourself, because no one else is going to do it for you.",
        "Great things never come from comfort zones.",
        "Dream it. Wish it. Do it.",
        "Success doesn’t just find you. You have to go out and get it.",
        "The harder you work for something, the greater you’ll feel when you achieve it."
    ]
    return random.choice(messages)

# Function to print motivational message
def send_motivational_message():
    message = get_motivational_message()
    speak(message)
    print("Motivational Message:", message)

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour <= 12:
        speak("Good Morning!")
    elif 12 <= hour <= 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("Welcome to Wellbot")
    print("Welcome to Wellbot")

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
    sentences = ai_response.split('. ')
    selected_sentences = '. '.join(sentences[:5])
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

def calculate_bmi(weight, height):
    bmi = weight / (height ** 2)
    return bmi

def interpret_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal weight"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def calculate_bmi_function():
    speak("Sure! Please provide your weight in kilograms.")
    response_text.config(state=tk.NORMAL)
    response_text.delete(1.0, tk.END)  # Clear the previous response
    response_text.insert(tk.END, "Please enter your weight in kilograms:\n")
    response_text.config(state=tk.DISABLED)
    response_text.see(tk.END)
    weight_entry = tk.Entry(root, width=20, font=("Arial", 12))
    weight_entry.grid(row=5, column=2, padx=(0, 5), pady=(5, 5))  # Adjust position
    weight_entry.focus_set()  # Set focus on the weight entry widget

    def get_weight():
        weight = weight_entry.get().strip()
        if weight:
            return float(weight)
        else:
            speak("Please enter your weight.")
            return None

    def on_weight_submit():
        weight = get_weight()
        if weight is not None:
            speak("Please provide your height in meters.")
            response_text.config(state=tk.NORMAL)
            response_text.insert(tk.END, "Please enter your height in meters:\n")
            response_text.config(state=tk.DISABLED)
            response_text.see(tk.END)
            height_entry = tk.Entry(root, width=20, font=("Arial", 12))
            height_entry.grid(row=6, column=2, padx=(0, 5), pady=(5, 5))  # Adjust position
            height_entry.focus_set()  # Set focus on the height entry widget

            def get_height():
                height = height_entry.get().strip()
                if height:
                    return float(height)
                else:
                    speak("Please enter your height.")
                    return None

            def on_height_submit():
                height = get_height()
                if height is not None:
                    bmi = calculate_bmi(weight, height)
                    category = interpret_bmi(bmi)
                    bmi_message = f"Your BMI is {bmi:.2f}. You are categorized as {category}."
                    speak(bmi_message)
                    response_text.config(state=tk.NORMAL)
                    response_text.insert(tk.END, bmi_message + '\n')
                    response_text.config(state=tk.DISABLED)
                    response_text.see(tk.END)
                    weight_entry.destroy()  # Remove weight entry widget
                    height_entry.destroy()  # Remove height entry widget

            height_entry.bind("<Return>", lambda event: on_height_submit())  # Bind Enter key to submit height
            height_entry.bind("<KP_Enter>", lambda event: on_height_submit())  # Bind Numpad Enter key to submit height

    weight_entry.bind("<Return>", lambda event: on_weight_submit())  # Bind Enter key to submit weight
    weight_entry.bind("<KP_Enter>", lambda event: on_weight_submit())  # Bind Numpad Enter key to submit weight




def fitness_plans():
    speak("Let's create your personalized fitness plan.")
    speak("What are your fitness goals? For example, weight loss, muscle gain, or general fitness.")
    fitness_goals = takeCommand()
    ai_response = chat.send_message(f"Generate a fitness plan for achieving {fitness_goals}").text
    sentences = ai_response.split('. ')
    selected_sentences = '. '.join(sentences[:5])
    speak("Here are the key points of your personalized fitness plan:")
    print("Generated Fitness Plan:", selected_sentences)
    speak(selected_sentences)


def get_fitness_info():
    speak("Let's create your personalized fitness plan.")
    speak("What are your fitness goals? For example, weight loss, muscle gain, or general fitness.")
    fitness_goals = takeCommand()
    other_info = "Other information related to fitness goals"
    return {'fitness_goals': fitness_goals, 'other_info': other_info}

def Stress_Buster():
    music_folder = r"G:\songs ncs"
    music_files = os.listdir(music_folder)
    music_files = [file for file in music_files if file.endswith('.mp3')]
    if not music_files:
        speak("No MP3 files found in the music folder.")
        return
    random_song = random.choice(music_files)
    song_path = os.path.join(music_folder, random_song)
    os.startfile(song_path)


def motivational_message():
    messages = [
        "Believe you can and you're halfway there. - Theodore Roosevelt",
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
        "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
        "Your limitation—it's only your imagination.",
        "Push yourself, because no one else is going to do it for you.",
        "Great things never come from comfort zones.",
        "Dream it. Wish it. Do it.",
        "Success doesn’t just find you. You have to go out and get it.",
        "The harder you work for something, the greater you’ll feel when you achieve it."
    ]
    message = random.choice(messages)
    speak("Here's a motivational message to keep you going:")
    speak(message)
    print("Motivational Message:", message)


experts = {
    'trainer': {
        'name': 'John Doe',
        'qualification': 'Certified Personal Trainer',
        'availability': {
            'monday': ['10:00 AM', '12:00 PM'],
            'wednesday': ['09:00 AM', '11:00 AM']
        }
    },
    'nutritionist': {
        'name': 'Alice Smith',
        'qualification': 'Registered Dietitian',
        'availability': {
            'tuesday': ['02:00 PM', '04:00 PM'],
            'thursday': ['03:00 PM', '05:00 PM']
        }
    }
}


def schedule_appointment(expert_type, preferred_time):
    # Check expert availability and schedule appointment
    expert = experts.get(expert_type)
    if expert:
        availability = expert.get('availability')
        if preferred_time in availability:
            # Schedule appointment and notify user
            speak(f"Appointment scheduled with {expert['name']} at {preferred_time}.")
        else:
            speak("Sorry, the preferred time slot is not available.")
    else:
        speak("Sorry, we couldn't find an expert of that type.")


def consult_expert():
    speak("Sure! Let's schedule an appointment with an expert.")
    speak("What type of consultation do you need? Trainer or nutrition advice?")
    expert_entry = tk.Entry(root, width=20, font=("Arial", 12))
    expert_entry.grid(row=5, column=2, padx=(0, 5), pady=(5, 5))  # Adjust position
    expert_entry.focus_set()  # Set focus on the expert entry widget

    def get_expert_type():
        expert_type = expert_entry.get().strip().lower()
        if expert_type:
            return expert_type
        else:
            speak("Please specify the type of consultation.")
            return None

    def on_expert_submit():
        expert_type = get_expert_type()
        if expert_type is not None:
            speak(f"Great! You've selected {expert_type}.")
            speak("Please provide your preferred day and time for the appointment.")
            datetime_entry = tk.Entry(root, width=20, font=("Arial", 12))
            datetime_entry.grid(row=6, column=2, padx=(0, 5), pady=(5, 5))
            datetime_entry.focus_set()

            def get_datetime():
                preferred_time = datetime_entry.get().strip()
                if preferred_time:
                    return preferred_time
                else:
                    speak("Please enter your preferred day and time.")
                    return None

            def on_datetime_submit():
                preferred_time = get_datetime()
                if preferred_time is not None:
                    schedule_appointment(expert_type, preferred_time)

            datetime_entry.bind("<Return>", lambda event: on_datetime_submit())
            datetime_entry.bind("<KP_Enter>", lambda event: on_datetime_submit())

    expert_entry.bind("<Return>", lambda event: on_expert_submit())
    expert_entry.bind("<KP_Enter>", lambda event: on_expert_submit())



def on_submit(selected_option):
    if 'Wikipedia' in selected_option:
        # Handle Wikipedia search
        speak("Searching Wikipedia...")
        query = selected_option.replace("Wikipedia", "")
        results = wikipedia.summary(query, sentences=5)
        speak("According to Wikipedia")
        speak(results)
    elif 'YouTube' in selected_option:
        # Handle YouTube open
        speak("Opening Youtube...")
        webbrowser.open("https://www.youtube.com/watch?v=xrnVAbZmBCk")
    elif 'Time' in selected_option:
        # Handle time query
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {strTime}")
    elif 'First Aid' in selected_option:
        # Handle first aid information
        speak("Providing first aid information")
        webbrowser.open("https://www.verywellhealth.com/basic-first-aid-procedures-1298578")
    elif 'Diet chart' in selected_option:
        # Handle diet and nutrition related queries
        nutrition_and_diet_management(selected_option)
    elif 'Fitness Plan' in selected_option:
        # Handle fitness plan generation
        fitness_plans()
    else:
        speak("Sorry, I didn't understand that command.")



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

input_label = tk.Label(root, text="May I Help You?:", font=("Arial", 14))
input_label.grid(row=0, column=1, padx=(0, 0), pady=(10, 5))

# Dropdown menu (Combobox)
options = ["Wikipedia", "YouTube", "Time", "First Aid", "Diet chart", "Fitness Plan"]
selected_option = tk.StringVar(root)
selected_option.set(options[0])  # Default value

select_menu = ttk.Combobox(root, textvariable=selected_option, values=options, width=30, font=("Arial", 12))
select_menu.grid(row=0, column=2, padx=(0, 0), pady=(10, 5))

#speak_button
listen_button = tk.Button(root, text="Speak", command=listen, width=10, height=1)
listen_button.grid(row=0, column=3, padx=(0, 5), pady=(10, 5))

# Submit button
submit_button = tk.Button(root, text="Submit", command=lambda: on_submit(selected_option.get()), width=15, height=2)
submit_button.grid(row=1, column=2, padx=(0, 0), pady=1)


# BMI button
bmi_button = tk.Button(root, text="Calculate BMI", command=calculate_bmi_function, width=15, height=2, bg="orange")
bmi_button.grid(row=2, column=1, padx=(0, 0), pady=20)

# Add button for expert consultation
consult_button = tk.Button(root, text="Consult Expert", command=consult_expert, width=15, height=2, bg="orange")
consult_button.grid(row=2, column=2, padx=(0,0), pady=20)

# Add button for playing a random song
Stress_Buster_button = tk.Button(root, text="Stress Buster", command=Stress_Buster, width=15, height=2, bg="orange")
Stress_Buster_button.grid(row=2, column=3, padx=(0,5), pady=20)

# Text box for response
response_label = tk.Label(root, text="RESPONSE:", font=("Arial", 14))
response_label.grid(row=3, column=1, padx=(1, 0), pady=10)
response_text = tk.Text(root, width=50, height=5, state='normal')
response_text.grid(row=3,column=2, padx=(0, 1), pady=10)


# Emergency button
emergency_button = tk.Button(root, text="Emergency", command=call_emergency_services, width=15, height=2)
emergency_button.grid(row=4, column=2, padx=(1, 0), pady=5)


listening = False
wishMe()  # Call the wishMe function to greet the user when the GUI is launched

greet_user()

bg_image = tk.PhotoImage(file="background.png")
background_label = tk.Label(root, image=bg_image)
background_label.place(relwidth=1, relheight=1)
background_label.lower()

root.mainloop()
