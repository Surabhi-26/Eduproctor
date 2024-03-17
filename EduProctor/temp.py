import json
testname = 'java'
fkey=''
with open('classrooms/surabhi.json', 'r') as file:
    data = json.load(file)
for student in data.get("students", []):
    # Check if the "name" key exists and its value is "java"
    if student.get("name") == "java":
        print("Key matching 'java':", student)

