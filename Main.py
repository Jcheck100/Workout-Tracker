import json
import os
import matplotlib.pyplot as plt
import pandas as pd
filename = "exercisedata.json"

# Loads existing data from the file exercisedata.json
def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            if isinstance(data, list):  # Ensure the loaded data is a list
                return data
    return []  # If no file exists or data is empty, return an empty list

# Saves data to the file exercisedata.json
def save_data(filename, exercises):
    with open(filename, 'w') as file:
        json.dump(exercises, file, indent=4)

# Initializes list of exercises
exercises = load_data(filename)

# Start collecting data
while True:
    getDate = str(input('Enter Date or q to quit: '))

    if getDate.lower() == "q":
        break
    else:
        num_exercises = int(input("Enter Number of exercises: "))
        
        # Iterate for each exercise entry
        for i in range(num_exercises):
            exercise_name = str(input('\nEnter Exercise: '))  # Exercise name
            sets = int(input('Enter Sets: '))
            reps = int(input('Enter Reps: '))
            weight = int(input('Enter Weight: '))

            # Create a dictionary for the current exercise data
            exercise_data = {
                'Date': getDate,
                'Exercise': exercise_name,
                'Sets': sets,
                'Reps': reps,
                'Weight': weight
            }

            # Append the exercise data to the exercises list
            exercises.append(exercise_data)

# After data collection, save the exercises data to exercisedata.json
save_data(filename, exercises)

# Makes dataframe so we can read data eaisily
df = pd.DataFrame(exercises)

# Prints the DataFrame to check what has been saved
print("\nExercise Data:")
print(df)
