

import os
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random

from flask import Flask, render_template, request, redirect,url_for

app = Flask(__name__)





def send_email(class_name,tempname):
    # Gmail account credentials
    gmail_user = 'tilekar.surabhi@gmail.com'  # Enter your Gmail email address
    gmail_password = 'aldz gzov odps ruyi'  # Enter your Gmail password

    # Retrieve email addresses of students from respective JSON file
    folder_path = 'classrooms'
    with open(os.path.join(folder_path, class_name + '.json'), 'r') as f:
        data = json.load(f)
        student_list = data.get('students', [])

    # Email content
    subject = 'Hello from Classroom'

    # Send email and assign passkey to each student
    for student in student_list:
        student_email = student['email']
        passkey = str(random.randint(1000, 9999))  # Generate a random 4-digit number
        body = f'Hello {student["name"]}, your  test  {tempname} of {class_name} is available Your passkey is: {passkey} '

        # Add passkey parameter to student data
        student['passkey'] = passkey

        # Email setup
        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = student_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            # Send email
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            server.sendmail(gmail_user, student_email, msg.as_string())
            server.close()
            print('Email sent successfully to', student_email)

            # Update JSON file with the new passkey
            with open(os.path.join(folder_path, class_name + '.json'), 'w') as f:
                json.dump(data, f)
                print('Passkey updated for', student_email)
        except Exception as e:
            print('Failed to send email to', student_email, ':', str(e))








classrooms = []
global classname,testid,classname3
classname = ''
@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        usertype = request.form.get('userType')
        email = request.form.get('email')
        passw = request.form.get('pass')
        if int(usertype)== 1 :
            if email == "admin@gmail.com" and passw == "123":
                return redirect('/admin')
        if int(usertype)==2:
            return redirect('/student')
        if int(usertype)== 3 :
            with open("database/teacher.json",'r') as f:
                data = json.load(f)

            if data[str(email)]== "123":

                return redirect('/teacher?email='+email)
    return render_template('index.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/student')
def student():
    return render_template('student.html')

@app.route('/createclass',methods = ['GET', 'POST'])
def createclass():
    if request.method == 'POST':
        name= classroom_name = request.form['classroom_name']
        classroom_code = request.form['classroom_code']
        teacher_email = request.form['finalstr'].split(',')

        # Check if the classroom already exists
        classroom_exists = False
        for cls in classrooms:
            if cls['name'] == classroom_name:
                classroom_exists = True
                cls['teacher'].extend(teacher_email)
                # Load the JSON file for the existing classroom
                filename = "classrooms/" + classroom_name + ".json"
                if os.path.exists(filename):
                    with open(filename, 'r+') as f:
                        data = json.load(f)
                        existing_emails = data.get("teacher", [])
                        # Add new emails to the existing list
                        for email in teacher_email:
                            if email not in existing_emails:
                                existing_emails.append(email)
                        # Update the JSON file with the combined list of emails
                        data["teacher"] = existing_emails
                        f.seek(0)
                        json.dump(data, f, indent=4)
                        f.truncate()
                break

        if not classroom_exists:
            # Classroom doesn't exist, add it to the list and create a new JSON file
            classrooms.append({'name': classroom_name, 'teacher': teacher_email})
            filename = "classrooms/" + classroom_name + ".json"
            with open(filename, 'w') as f:
                json.dump({"teacher": teacher_email,"class_code":classroom_code,"class_name":name}, f, indent=4)

    return render_template('createclass.html', classrooms=classrooms)


@app.route('/delete',methods = ['GET', 'POST'])
def delete():
    if request.method == 'POST':
        classname = request.form.get('class')
        if os.path.exists('classrooms/'+classname+'.json'):
            os.remove('classrooms/'+classname+'.json')
    folder_path = 'classrooms'
    file_names = os.listdir(folder_path)

    temp = []
    for file in file_names:
        temp.append(file[0:-5])
    return render_template('delete.html',temp=temp)

@app.route('/teacher', methods=['GET'])
def teacher():
    teacher_email = request.args.get('email')

    folder_path = 'classrooms'
    file_names = os.listdir(folder_path)

    teacher_classrooms = []
    for file_name in file_names:
        if file_name.endswith('.json'):
            # Extract the classroom name from the file name
            classroom_name = file_name[:-5]  # Remove the ".json" extension

            # Read the JSON file and extract the teacher emails
            with open(os.path.join(folder_path, file_name), 'r') as f:
                data = json.load(f)
                if teacher_email in data.get('teacher', []):
                    teacher_classrooms.append(classroom_name)

    print(teacher_classrooms)
    with open("classrooms/"+teacher_classrooms[0]+".json", "r") as f:
        data = json.load(f)
        name = data["class_name"]
        code = data["class_code"]
    return render_template('teacher.html', classrooms=teacher_classrooms,code=code,name=name,mail=teacher_email)


@app.route('/createtest',methods = ['GET', 'POST'])
def test():
    global classname,testid
    if  request.method == 'POST':

        qtype = request.form.get('type')
        if qtype == '1':
            level = request.form.get('level')
            que = request.form.get('que')
            op1 = request.form.get('op1')
            op2 = request.form.get('op2')
            op3 = request.form.get('op3')
            op4 = request.form.get('op4')
            answer = request.form.get('answer')
            print(testid)
            data_dict = {"level":level,"que":que,"op1":op1,"op2":op2,"op3":op3,"op4":op4,"answer":answer}
            with open('classrooms/'+classname+'.json','r') as r:
                data = json.load(r)
            data[str(testid)]["mcq"].append(data_dict)
            with open('classrooms/' + classname + '.json', 'w') as g:
                json.dump(data, g)



        elif qtype == '2':
            level = request.form.get('level')
            que = request.form.get('que')

            data_dict = {"level": level, "que": que}
            with open('classrooms/' + classname + '.json', 'r') as r:
                data = json.load(r)
            data[str(testid)]["text"].append(data_dict)
            with open('classrooms/' + classname + '.json', 'w') as g:
                json.dump(data, g)

        elif qtype == '3':
            level = request.form.get('level')
            que = request.form.get('que')
            t1 = request.form.get('t1')
            a1 = request.form.get('a1')
            t2 = request.form.get('t2')
            a2 = request.form.get('a2')

            data_dict = {"level": level, "que": que, "t1": t1, "a1": a1,"t2": t2, "a2": a2}
            with open('classrooms/' + classname + '.json', 'r') as r:
                data = json.load(r)
            data[str(testid)]["code"].append(data_dict)
            with open('classrooms/' + classname + '.json', 'w') as g:
                json.dump(data, g)
        else:
            pass




    return render_template('createtest.html')

@app.route('/listtest',methods = ['GET', 'POST'])
def listtest():
    global classname,testid
    if request.method == 'POST':

        name = request.form.get('name')
        id = request.form.get('id')

        time = request.form.get('time')
        mark = request.form.get('mark')
        date = request.form.get('date')


        with open('classrooms/'+str(classname)+'.json', 'r') as file:
            data = json.load(file)

        # Add new data to the JSON dictionary
        data[id] = {"name": name,"status":"notreleased", "id": id, "time": time, "marks": mark,"date": date, "mcq": [], "text": [], "code": []}

        # Write the updated data back to the JSON file
        with open('classrooms/'+classname+'.json', 'w') as file:
            json.dump(data, file)

    newdict = {}
    with open('classrooms/'+classname+'.json', 'r') as file:
        data = json.load(file)
    for key, value in data.items():
        # Check if the item is a dictionary (excluding the "teacher" key)
        if isinstance(value, dict) and key != "teacher":
            # Add name and id to the new dictionary
            newdict[value["name"]] = value["id"]
    return render_template('tests.html', newdict=newdict,filename=classname)

@app.route('/teacher-section',methods = ['GET', 'POST'])
def teachersec():
    global classname
    if request.method == 'POST':
        classcode1 = request.form.get('classroom_code')
        mail = request.form.get('mail')
        classname = classcode1
    return render_template('teacher2.html',code=classcode1,mail=mail)


@app.route('/redirect',methods = ['GET', 'POST'])
def redir():
    global classname,testid
    if request.method == 'POST':
        key = request.form.get('key')
        testid = key
        print("test id is "+testid)

    return redirect('/createtest')


@app.route('/changestatus',methods = ['GET','POST'])
def changestatus():
    global classname,testid

    if request.method == 'POST':
        with open('classrooms/'+classname+'.json', 'r') as file:
            data =json.load(file)
        data[str(testid)]["status"]='released'
        tempname = data[str(testid)]["name"]

        with open('classrooms/'+classname+'.json', 'w') as file:
            json.dump(data,file)

        send_email(classname,tempname)



    return redirect('/listtest')



@app.route('/join-class', methods=['POST'])
def join():
    return render_template('JoinClass.html')

@app.route('/join-classroom', methods=['POST'])
def join_classroom():
    global classname3
    classroom_code = request.form['classroom_code']

    # Check if the classroom code matches any existing classroom
    folder_path = 'classrooms'
    file_names = os.listdir(folder_path)
    for file in file_names:
        with open(os.path.join(folder_path, file), 'r') as f:
            data = json.load(f)
            if 'class_code' in data and data['class_code'] == classroom_code:
                # Classroom found, add student to the classroom
                student_name = "ishan"
                student_email = "Ishanapardeshi@gmail.com"
                classname3 = file
                if "students" not in data.keys():
                    data["students"]=[]
                data['students'].append({'name': student_name, 'email': student_email})

                # Update the JSON file with the new student
                with open(os.path.join(folder_path, file), 'w') as f:
                    json.dump(data, f)

                return redirect(url_for('classroom_joined'))

    # If the classroom code doesn't match any existing classroom, show error message
    return render_template('index.html', error="Invalid classroom code. Please try again.")

@app.route('/classroom-joined')
def classroom_joined():
    return "You have successfully joined the classroom!"

@app.route('/exam-pending',methods=['GET','POST'])
def exam_pending():
    global classname3

    if request.method=='POST':
        list =[]
        with open('classrooms/surabhi.json', 'r') as file:
            data = json.load(file)
            for key, value in data.items():
                # Check if the item is a dictionary (excluding the "teacher" key)
                if isinstance(value, dict):
                    if value['status']=='released':
                        list.append(
                            value['name']
                        )

        print(list)
    return render_template("exampending.html",exams=list)


@app.route('/start', methods=['GET'])
def startExam():
    testname = request.args.get('testname')


    return render_template('startExam.html',testname=testname)

@app.route('/mainexam',methods=['GET'])
def mainexam():
    mcq_data=[]
    testname =request.args.get('testname')
    fkey=''

    with open('classrooms/surabhi.json', 'r') as file:
        data = json.load(file)
    for student in data.get("students", []):
        # Check if the "name" key exists and its value is "java"
        if student.get("name") == testname:
            fkey=student
    return render_template('exam_main.html',item=data[str(fkey)])

app.run(debug=True)

