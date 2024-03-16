import os
import json
from flask import Flask, render_template, request

app = Flask(__name__)

classrooms = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        classroom_name = request.form['classroom_name']
        teacher_email = request.form['finalstr'].split(',')

        # Check if the classroom already exists
        classroom_exists = False
        for cls in classrooms[:]:  # Iterate over a copy of the classrooms list
            if cls['name'] == classroom_name:
                # Classroom exists, append teacher email to its list of teachers
                cls['teacher'].extend(teacher_email)
                classroom_exists = True
                break

        if not classroom_exists:
            # Classroom doesn't exist, add it to the list
            classrooms.append({'name': classroom_name, 'teacher': teacher_email})

        filename = "classrooms/" + classroom_name + ".json"

        # Create the 'classrooms' directory if it doesn't exist
        if not os.path.exists("classrooms"):
            os.makedirs("classrooms")

        if not os.path.exists(filename):
            # If the file doesn't exist, initialize it with empty "teacher" list
            with open(filename, 'w') as g:
                json.dump({"teacher": [1]}, g)

        with open(filename, 'r+') as f:
            # Load existing data or initialize with empty "teacher" list if the file was just created
            data = f.read()
            val = json.loads(data)
            val["teacher"].extend(teacher_email)
            f.seek(0)  # Move the cursor to the beginning of the file
            json.dump(val, f)
            f.truncate()  # Truncate any remaining data (in case the new data is shorter than the old data)

    return render_template('admin.html', classrooms=classrooms)

@app.route('/teacher', methods=['GET'])
def teacher():
    teacher_email = request.args.get('email')

    teacher_classrooms = [cls['name'] for cls in classrooms if teacher_email in cls['teacher']]

    return render_template('teacher.html', teacher_email=teacher_email, classrooms=teacher_classrooms)

if __name__ == '__main__':
    app.run(debug=True)
