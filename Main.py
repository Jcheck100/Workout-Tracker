import os
import json
import pandas as pd
import datetime
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

filename = 'exercisedata.json'
today = datetime.date.today()
now = today.strftime("%m-%d-%y")
coordinate = 150

def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
    return []

def save_data(filename, exercises):
    with open(filename, 'w') as file:
        json.dump(exercises, file, indent=4)

exercises = load_data(filename)

def submit():
    global coordinate
    exercises_data = []

    # Iterate through each exercise entry field
    for i in range(int(num_exercises_entry.get())):
        exercise_name = exercise_name_entries[i].get()
        sets = sets_entries[i].get()
        reps = reps_entries[i].get()
        weight = weight_entries[i].get()

        # Check if the exercise already exists for today's date
        existing_entry = next((entry for entry in exercises if entry['Date'] == now and entry['Exercise'] == exercise_name), None)
        
        if existing_entry:
            # If the exercise exists for the same day, update the entry
            existing_entry['Sets'] = sets
            existing_entry['Reps'] = reps
            existing_entry['Weight'] = weight
        else:
            # If the exercise doesn't exist, add a new entry
            exercise_data = {
                'Date': now,
                'Exercise': exercise_name,
                'Sets': sets,
                'Reps': reps,
                'Weight': weight
            }
            exercises_data.append(exercise_data)

    # Add or update the exercises data in the main list
    exercises.extend(exercises_data)
    save_data(filename, exercises)

    print("\nExercise Data saved to JSON:")
    df = pd.DataFrame(exercises)
    print(df)

    update_exercise_options()

def create_input_fields():
    global coordinate
    num_exercises = int(num_exercises_entry.get())

    for entry in exercise_name_entries:
        entry.destroy()
    for entry in sets_entries:
        entry.destroy()
    for entry in reps_entries:
        entry.destroy()
    for entry in weight_entries:
        entry.destroy()
    coordinate = 150

    for i in range(num_exercises):
        
        name_label = ctk.CTkLabel(root, text="Exercise:", width=120)
        sets_label = ctk.CTkLabel(root, text="Sets:", width=120)
        reps_label = ctk.CTkLabel(root, text="Reps:", width=120)
        weight_label = ctk.CTkLabel(root, text="Weight:", width=120)
        exercise_name_entry = ctk.CTkEntry(root, width=100)
        sets_entry = ctk.CTkEntry(root, width=100)
        reps_entry = ctk.CTkEntry(root, width=100)
        weight_entry = ctk.CTkEntry(root, width=100)

        name_label.place(x=5, y=120)
        sets_label.place(x=145, y=120)
        reps_label.place(x=295, y=120)
        weight_label.place(x=450, y=120)
        exercise_name_entry.place(x=40, y=coordinate)
        sets_entry.place(x=190, y=coordinate)
        reps_entry.place(x=340, y=coordinate)
        weight_entry.place(x=490, y=coordinate)

        exercise_name_entries.append(exercise_name_entry)
        sets_entries.append(sets_entry)
        reps_entries.append(reps_entry)
        weight_entries.append(weight_entry)

        coordinate += 60

def update_exercise_options():
    # Update the exercise dropdown with unique exercises from the loaded data
    unique_exercises = list(set([entry['Exercise'] for entry in exercises]))
    exercise_select.configure(values=unique_exercises)

def plot_data():
    exercise_to_plot = exercise_select.get()

    df = pd.DataFrame(exercises)
    df['Weight'] = pd.to_numeric(df['Weight'], errors='coerce')
    df['Date'] = pd.to_datetime(df['Date'], format="%m-%d-%y")

    # Filter data for the selected exercise
    df_filtered = df[df['Exercise'] == exercise_to_plot]

    if df_filtered.empty:
        print(f"No data found for {exercise_to_plot}")
        return 

    plt.figure(figsize=(10, 6))
    plt.plot(df_filtered['Date'], df_filtered['Weight'], marker='o', color='b', linestyle='-', markersize=6)

    plt.xlabel('Date')
    plt.ylabel('Weight Lifted (lbs)')
    plt.title(f'{exercise_to_plot} Weight Lifted Over Time')

    # Formatting x-axis to show only the date without time, and rotating for readability
    plt.xticks(df_filtered['Date'], df_filtered['Date'].dt.strftime('%m-%d-%y'), rotation=45)

    plt.tight_layout()

    # Displaying the plot in Tkinter window
    canvas = FigureCanvasTkAgg(plt.gcf(), master=root) 
    canvas.draw()
    canvas.get_tk_widget().place(x=1600, y=150) 

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.title("Workout Tracker")
root.geometry("1920x1080")

# List to hold the entry fields for exercises
exercise_name_entries = []
sets_entries = []
reps_entries = []
weight_entries = []

num_exercises_entry = ctk.CTkEntry(root, width=75, justify='center')
num_exercises_entry.place(x=170, y=40)


num_exercises_label = ctk.CTkLabel(root, text="Number of exercises:")
num_exercises_label.place(x=40, y=40)


btn = ctk.CTkButton(root, text="Create Input Fields", command=create_input_fields)
btn.place(x=35, y=80)


submit_btn = ctk.CTkButton(root, text="Submit Data!", command=submit)
submit_btn.place(x=180, y=80)


exercise_select = ctk.CTkOptionMenu(root, values=["Progress to Graph"],)
exercise_select.place(x=470, y=80)


plot_btn = ctk.CTkButton(root, text="Plot Exercise Data", command=plot_data)
plot_btn.place(x=325, y=80)


update_exercise_options()

root.mainloop()

#TODO List
#Add User and Pass
#Data Encryption
#Improve UI
#Error Handeling
#Input Validation
