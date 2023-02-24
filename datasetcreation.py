import csv
import random

# Define the headers for the CSV file
headers = ['semester', 'faculty', 'attendance score',
           'assignment score', 'assessment score', 'results']

# Generate random data for 100,000 rows
data = []
for i in range(100000):
    semester = random.randint(1, 8)  # 1-8 denotes the semesters
    # 1-civil,2-computer,3-electronics,4-electrical
    faculty = random.randint(1, 4)
    attendance_score = round(random.uniform(0, 1), 2)
    assignment_score = round(random.uniform(0, 1), 2)
    assessment_score = round(random.uniform(0, 1), 2)
    # results = 'Pass' if (attendance_score + assignment_score +
    #                    assessment_score) >= 2.0 else 'Fail'
    if ((attendance_score+assessment_score+assignment_score)/3 >= 0.85):
        results = 1  # pass with good marks
    elif((attendance_score+assessment_score+assignment_score)/3 >= 0.7 < 0.85):
        results = 2  # can pass the exams
    elif((attendance_score+assessment_score+assignment_score)/3 >= 0.6 < 0.7):
        results = 3  # might pass the exam with just passing marks need more preperations to pass for sure
    elif((attendance_score+assessment_score+assignment_score)/3 >= 0.45 < 0.6):
        results = 4  # high chance of failing is one or two subjects but if prepared well can pass with passing marks
    elif((attendance_score+assessment_score+assignment_score)/3 >= 0.2 < 0.45):
        # will fail the exam might cover important topics only for better chance of passing
        results = 5
    else:
        # high chance of failing in most of subjects,better to leave one or two subjects to focus on rest
        results = 6
    data.append([semester, faculty, attendance_score,
                assignment_score, assessment_score, results])

# Write the data to a CSV file
with open('data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(data)
