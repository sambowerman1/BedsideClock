import csv

# Open the CSV file and read the data
with open('workout_schedule (1).csv', 'r') as f:
    reader = csv.reader(f)
    workoutlist = list(reader)

# Now 'workouts' is a list of lists, each containing a row of the CSV file
if __name__ == "__main__":
    print('Date')
    for i in range(len(workoutlist)):
        print(workoutlist[i][0])
    print('Workout')
    for i in range(len(workoutlist)):
        print(workoutlist[i][1])