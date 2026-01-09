import csv
import random
from datetime import datetime, timedelta

# Data pools
first_names = ['John','Jane','Mike','Sarah','David','Emma','Chris','Lisa','Tom','Anna','Robert','Emily','James','Olivia','William']
last_names = ['Smith','Johnson','Williams','Brown','Jones','Garcia','Miller','Davis','Wilson','Moore','Taylor','Anderson','Thomas']
countries = ['USA','UK','Canada','Germany','France','Australia','India','Japan','Brazil','Mexico']
cities = ['New York','London','Toronto','Berlin','Paris','Sydney','Mumbai','Tokyo','Sao Paulo','Mexico City']
departments = ['IT','HR','Finance','Marketing','Sales','Operations','Legal','R&D','Support','Admin']
job_titles = ['Manager','Analyst','Developer','Designer','Coordinator','Specialist','Director','Associate','Lead','Consultant']
education_levels = ['Bachelor','Master','PhD','High School','Associate','MBA','Diploma']
statuses = ['Active','On Leave','Probation','Contract','Remote']

headers = [
    'ID','First_Name','Last_Name','Email','Phone','Age','Gender','Country',
    'City','Address','Zip_Code','Department','Job_Title','Salary','Hire_Date',
    'Years_Experience','Education','Performance_Score','Projects_Completed',
    'Training_Hours','Satisfaction_Score','Attendance_Rate','Manager_ID','Team_Size','Status'
]

with open('sample_data_100x25.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    
    for i in range(1, 101):
        first = random.choice(first_names)
        last = random.choice(last_names)
        row = [
            i,
            first,
            last,
            f"{first.lower()}.{last.lower()}{i}@email.com",
            f"+1-{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}",
            random.randint(22, 65),
            random.choice(['Male', 'Female']),
            random.choice(countries),
            random.choice(cities),
            f"{random.randint(100, 9999)} Main Street",
            random.randint(10000, 99999),
            random.choice(departments),
            random.choice(job_titles),
            random.randint(30000, 150000),
            (datetime.now() - timedelta(days=random.randint(100, 3000))).strftime('%Y-%m-%d'),
            random.randint(1, 20),
            random.choice(education_levels),
            round(random.uniform(1, 5), 1),
            random.randint(1, 50),
            random.randint(10, 200),
            round(random.uniform(1, 10), 1),
            round(random.uniform(85, 100), 1),
            random.randint(1, 20),
            random.randint(1, 15),
            random.choice(statuses)
        ]
        writer.writerow(row)

print("✅ File 'sample_data_100x25.csv' created successfully!")