import ast
from email.mime.application import MIMEApplication
import pytz
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from datetime import datetime
from flask import Flask, flash, jsonify,redirect,render_template, send_file,session,request
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import hashlib
import qrcode
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
app = Flask(__name__)
app.secret_key = "sskey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///campus.db'
indian_timezone = pytz.timezone('Asia/Kolkata')
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True,nullable = False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    student_id = db.Column(db.String, unique=False)
    department = db.Column(db.String, unique= False)
    cls = db.Column(db.String, unique=False)
    phoneno = db.Column(db.String, unique=False)
    email = db.Column(db.String)
    company = db.Column(db.String, unique=False,nullable = True)
    date = db.Column(db.String, default=datetime.utcnow)
    hash = db.Column(db.String, unique=False,nullable = True)
    attendance= db.Column(db.String, unique=False,nullable = True,default="absent")
    placed = db.Column(db.String, unique=False,nullable = True)
    
    # Define the one-to-many relationship with Post
    subadmin = db.relationship('SubAdmin', backref='author', lazy=True)

    coordinator = db.relationship('Coordinator', backref='author', lazy=True)

    campus = db.relationship('Campus', backref='author', lazy=True)

    ArchivedCampus = db.relationship('ArchivedCampus', backref='author', lazy=True)

class SubAdmin(db.Model):
    sno = db.Column(db.Integer, primary_key=True,nullable = True)
    name = db.Column(db.String)
    loginid =db.Column(db.String, unique=True)
    password = db.Column(db.String, unique=False)
    campus = db.Column(db.String,unique=False,nullable=True)
    date = db.Column(db.String,unique=False,nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=True)



class Coordinator(db.Model):
    sno = db.Column(db.Integer, primary_key=True,nullable = True)
    name = db.Column(db.String)
    loginid =db.Column(db.String, unique=True)
    password = db.Column(db.String, unique=False)
    campus = db.Column(db.String,unique=False,nullable = True)
    date = db.Column(db.String,unique=False,nullable = True)

    user_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=True)

class Campus(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    departments = db.Column(db.String, nullable=True)
    pack = db.Column(db.String, nullable=True)
    date = db.Column(db.String, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=True)
 
class ArchivedCampus(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    departments = db.Column(db.String, nullable=True)
    pack = db.Column(db.String, nullable=True)
    date = db.Column(db.String, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=True)
 

@app.route("/")
def home():
    user = session.get('user')
    if user and user == 'admin':
        dept = []
        ca = Campus.query.all()
        for dep in ca:
            dept.append(ast.literal_eval(dep.departments))

        zp = zip(ca,dept)
        return render_template("index.html",zp=zp,campus = ca)
    
    return  redirect("/login")

@app.route("/campusReport")
def creport():
    user = session.get('user')
    if user and user == 'admin':
        dept = []
        ca = Campus.query.all()
        for dep in ca:
            dept.append(ast.literal_eval(dep.departments))

        zp = zip(ca,dept)
        return render_template("campusreport.html",zp=zp)
    
    return  redirect("/login")

@app.route("/adminReport")
def adminReport():
    user = session.get("user")
    if user and user == "admin":
        admins = SubAdmin.query.all()
        return render_template("adminlist.html",admins = admins)
    return  redirect("/login")

@app.route("/coordinatorReport")
def coordinatorReport():
    user = session.get("user")
    if user and user == "admin":
        admins = Coordinator.query.all()
        return render_template("colist.html",admins = admins)
    return  redirect("/login")

@app.route("/archivedCampusReport")
def acreport():
    user = session.get('user')
    if user and user == 'admin':
        dept = []
        ca = ArchivedCampus.query.all()
        for dep in ca:
            dept.append(ast.literal_eval(dep.departments))

        zp = zip(ca,dept)
        return render_template("archivedCampus.html",zp=zp)
    
    return  redirect("/login")

@app.route("/veiwStats/<string:cam>")
def viewStats(cam):
    user = session.get('user')
    if user and user == 'admin':
        updateAttendance(cam)
        st = Campus.query.filter(Campus.name == cam).first()
        departments = st.departments
        departments = ast.literal_eval(departments)
        # print(departments)
        return render_template("stats.html",departments = departments,st=st)
    
    return  redirect("/login")
    
def updateAttendance(cam):
    
    c = Campus.query.filter(Campus.name == cam).first()
    department_names = ["clg","IT", "CSD", "CSE", "AIML", "CT", "AIDS", "EL", "EE", "ETC", "ME", "CE", "IIOT"]
    dept = c.departments
    dept = ast.literal_eval(dept)
    for department_name in department_names:
       
        if(department_name == 'clg'):
            p = Student.query.filter(Student.company == cam,Student.attendance == "present").all()
            a = Student.query.filter(Student.company == cam,Student.attendance == "absent").all()
            dept[department_name]['present'] =  len(p)
            dept[department_name]['absent'] =  len(a)
        else:

            p = Student.query.filter(Student.company == cam,Student.attendance == "present",Student.department == department_name).all()
            a = Student.query.filter(Student.company == cam,Student.attendance == "absent",Student.department == department_name).all()
            dept[department_name]['present'] =  len(p)
            dept[department_name]['absent'] =  len(a)

    c.departments = str(dept)
  
    db.session.add(c)
    db.session.commit()


@app.route("/subadmin",methods = ['GET','POST'])
def subadmin():
    user = session.get('user')
    if user and user == 'admin':

        if request.method == 'POST':
            role = request.form['role']
            name = request.form['name']
            id = request.form['id']
            password = request.form['password']

            if role == 'subadmin':
                sadmin = SubAdmin(name = name,loginid = id,password = password)
            else:
                sadmin = Coordinator(name = name,loginid = id,password = password)

            db.session.add(sadmin)
            db.session.commit()

            return redirect("/subadmin")
        return render_template("subadmin.html")
    return  redirect("/login")

def xlswork(file, campus):
    file.save(file.filename)
    
    if file.filename == '':
        # print("here")
        return 'No selected file'

    try:
        
        # Read the XLS file into a DataFrame
        df = pd.read_excel(file)
    
        # Iterate through the rows and insert data into the database
        for _, row in df.iterrows():
            
            name = row['Name of Student']
            student_id = row['College ID']
            department = row['Branch']
            email = f"{student_id}@ycce.in"
            campusDate = row['Date']
            cls = row['Section']
            venue = row['Lab']
            reportingtime = row['Reporting Time']
            reportingtime= str(reportingtime)

            hash_value = hashlib.sha256(f"{name}{student_id}{department}".encode()).hexdigest()

            student = Student(
                name=name,department=department,cls=cls,phoneno = reportingtime,email=email, hash=hash_value,student_id = student_id,company = campus
                
            )
    
        
            admitcardpath = createADmit(student_id,name,reportingtime,campusDate,department,email,venue,hash_value,campus)
            
            send_email(email, admitcardpath,campus,name,campusDate,venue,reportingtime)
            db.session.add(student)
            
        db.session.commit()

        return 'Data uploaded successfully'
    except Exception as e:
        return f'Error: {str(e)}'
 

def createADmit(studentid,name,reportingtime,campusdate,department,email,venue,hashvalue,campus):
    pdf_file = f"admitcards/{studentid}.pdf"
    c = canvas.Canvas(pdf_file, pagesize=letter)
    # Set font sizes
    title_font_size = 20
    info_font_size = 15

    # Set starting positions
    x = 50
    y = 740  # Start from the top of the page


    left_x = 20 # Adjust as needed
    right_x = letter[0] - 20  # Adjust as needed
    top_y = letter[1] - 20 # Adjust as needed
    bottom_y = 20  # Adjust as needed

    c.line(left_x, top_y, right_x, top_y)
    c.line(left_x, bottom_y, right_x, bottom_y)
    c.line(left_x, top_y, left_x, bottom_y)
    c.line(right_x, top_y, right_x, bottom_y) 
    fields = [
        ('Yeshwantrao Chavan College of Engineering', ''),
        ('College ID', studentid),
        ('Full Name', name),
        ('Department', department),
        ('Email', email),
        ('Date ', campusdate),
        ('Degree', f'B. Tech. ({department})'),
        ('Reporting Time ', reportingtime),
        ('Venue ', venue),
    ]
   
    # Iterate through fields and add them to the PDF
    for field_name, field_value in fields:
        if field_name == 'Yeshwantrao Chavan College of Engineering':
            print("here4")
            c.setFont("Helvetica", 12)
            c.setFillColor(colors.black)
            c.drawString(200, y, "Nagar Yuwak Shikshan Sanstha's")
            y-=19
            font_size = title_font_size
            font_color = colors.blue
            c.setFont("Helvetica", font_size)
            c.setFillColor(font_color)
            c.drawString(x+50, y, f'{field_name}')
            y -= 16
            c.setFont("Helvetica-Oblique", 13)
            c.setFillColor(colors.red)
            c.drawString(x, y, "(An Autonomous Institution affiliated to Rashtrasant Tukadoji Maharaj Nagpur University)")
            y-=16
            c.setFont("Helvetica", 13)
            c.setFillColor(colors.brown)
            c.drawString(200, y, "(Accredited 'A' Grade by NAAC)")
            y-=19
             # Adjust position below the last field
            #  c.line(left_x, top_y, right_x, top_y)
            c.line(left_x, y+10, right_x, y+10)
            y-=30
            c.setFont("Helvetica-Bold", font_size)
            c.setFillColor(colors.blue)
            c.drawString(x, y, f'Student Admit Card')
            y -= 40 


        else:
            font_size = info_font_size
            font_color = colors.black 
            c.setFont("Helvetica", font_size)
            c.setFillColor(font_color)
            c.drawString(x, y, f'{field_name}  :       {field_value}')
            y -= 30  
        
        # Adjust the vertical position for the next field
    c.setFont("Helvetica-Bold", font_size)
    c.setFillColor(colors.blue)
    c.drawString(x, y, "General Guidelines:")
    y -= 20
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)
    c.drawString(x, y, '''Candidate may not be permitted in future processes and will be disqualified from any stage of our process if found:'''
)
    y-=15
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)
    c.drawString(x, y, '''1. Not meeting eligibility criteria at any stage of the process (registration, selection and onboarding)'''
)
    y-=15
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)
    c.drawString(x, y, '''2. Insufficient and ambiguous documents produced or submitted'''
)
    y-=15
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)
    c.drawString(x, y, '''3.Candidate found indulging in any malpractice/ falsified information during our process'''
)
    y-=20

    c.setFont("Helvetica-Bold", font_size-5)
    c.setFillColor(colors.gray)
    c.drawString(x, y, "Specifically for communication assessment::")
    y-=20
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)
    c.drawString(x, y, '''1. It's highly recommended to use a USB enabled Headset with a microphone, or a good quality headset with single '''
)
    y-=15
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)
    c.drawString(x, y, '''jack – 3.5mm having microphone'''
)
    y-=15

    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)
    c.drawString(x, y, '''2. Students must avoid using Bluetooth headsets or using on system speakers and microphone'''
)
    y-=20

    c.setFont("Helvetica-Bold", font_size-5)
    c.setFillColor(colors.gray)
    c.drawString(x, y, "About Gadgets:")
    y-=20

    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)
    c.drawString(x, y, '''1. The Online Test of Avaali Solutions Pvt Ltd. is scheduled as per details given the attached list. Students will report'''
)
    y-=15

    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)
    c.drawString(x, y, '''for the Online Test as per the date, time & venue mentioned. No deviation is permitted.'''
)
    y-=15

    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)
    c.drawString(x, y, '''2. Students to report at the allotted Lab 30 mins prior to Test Time.'''
)
    y-=15

    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)
    c.drawString(x, y, '''3. Students will be in College Uniform.'''
)
    y-=15

    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)
    c.drawString(x, y, '''4. Carry OWN LAPTOP with resume saved on Desktop. Carry College ID Card Aadhar Card.'''
)
    y-=15

    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)
    c.drawString(x, y, '''5. No Electronic Gadgets allowed during the Online Test'''
)
    y-=15

    # Generate QR code
    qr_data = hashvalue
    qr = qrcode.make(qr_data)
    qr.save('qrcode.png')

    # Draw the QR code onto the PDF
    c.drawImage('qrcode.png', x + 375, 455, width=150, height=150)
    c.setFont("Helvetica", 15)
    c.setFillColor(colors.black)
    c.drawString(x+400, 450, f'{campus}')

    # Save the PDF document
    c.save()
    # Create a PDF document
    print('Your ID Card has been successfully created as "ID_Card.pdf"')

    return pdf_file

@app.route("/createCampus", methods=['GET', 'POST'])
def camp():
    sa = SubAdmin.query.all()
    co = Coordinator.query.all()
    ca = Campus.query.all()
    user = session.get('user')
    id = SubAdmin.query.filter(SubAdmin.loginid == user).first()
    if user and (user == 'admin' or user == id.loginid):

        if request.method == 'POST':
            role = request.form["role"]
            campus = request.form['campus']
            admin_id = request.form['admin_id']
            # admin_id = admin_id[1:len(admin_id)-1]
            date = request.form['date']
            file = request.files['file']
            a = xlswork(file,campus)
            print(a)
            if role == "subadmin":
                ad = SubAdmin.query.filter_by(loginid = admin_id).first()
            else : 
                ad = Coordinator.query.filter_by(loginid = admin_id).first()

            ad.campus = campus
            ad.date = date

            db.session.add(ad)
            db.session.commit()
            updateCampus(campus)
            return redirect("/createCampus")

        s = []
        c = []
        for a in sa:
            s.append(a.loginid)
            
            # Check if a file was uploaded
        for b in co:
            c.append(b.loginid)
    

        return render_template("campus.html",campus = ca,subadmin = str(s),coordinator = str(c) )
    
    
    return  redirect("/login")

    
def updateCampus(campus):
    ca = Campus.query.filter(Campus.name == campus).first()
    departments = ca.departments
    departments = ast.literal_eval(departments)
    department_names = ["clg","IT", "CSD", "CSE", "AIML", "CT", "AIDS", "EL", "EE", "ETC", "ME", "CE", "IIOT"]
    department_students = {}

    for department_name in department_names:
       
        if(department_name == 'clg'):
            query = Student.query.filter(Student.company == campus).all()
            departments[department_name]['total'] =  len(query)
        else:

            query = Student.query.filter(Student.company == campus, Student.department == department_name).all()
        

            departments[department_name]['total'] =  len(query)
            department_students[department_name] = query
    
        
    ca.departments = str(departments)
  
    db.session.add(ca)
    db.session.commit()
  
    
def send_email(receiver_email,pdf_path,campus,name,campusdate,venue,reportingtime):
    subject = f"Admit Card  for {campus}"
    body = f"Dear {name},\n\nI wanted to remind you about our upcoming campus event tomorrow. Don't forget to bring your admit card for a smooth registration process.\n\nWishing you all the best of luck! You've got this!\n\nCampus Details:\nCompany Name : {campus}\nDate : {campusdate}\nLocation :{venue}\nReporting Time : {reportingtime}\n\nSee you there!\n\nBest regards\n\nT&P Cell YCCE."

    message = MIMEMultipart()
    message["From"] = "21070442@ycce.in"  # Replace with your email address
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Attach the PDF file to the email
    with open(pdf_path, "rb") as pdf_file:
        pdf_attachment = MIMEApplication(pdf_file.read(), name=os.path.basename(pdf_path))
        message.attach(pdf_attachment)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    try:
        # Connect to the SMTP server with TLS
        
        server.starttls()

        # Log in to the SMTP server with your email credentials
        server.login("21070442@ycce.in", "eaewfhklfijlhfuj")  # Replace with your email and password

        # Send the email
        server.sendmail("", receiver_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection to the SMTP server
        server.quit()


@app.route("/addCampus",methods = ['GET','POST'])
def addcamp():
    user = session.get('user')
    if user and user == 'admin':

        if request.method == "POST":
            name = request.form['name']
            date = request.form['date']
            pack = request.form['pack']
            departments = str({
                "clg":{
                "total":None,
                "present":None,
                "absent":None,
                "placed":None
                },
                "IT":{
                "total":None,
                "present":None,
                "absent":None,
                "placed":None
                },
                "CSD":{
                "total":None,
                "present":None,
                "absent":None,
                "placed":None
                },
                "CSE":{
                "total":None,
                "present":None,
                "absent":None,
                "placed":None
                },
                "AIML":{
                "total":None,
                "present":None,
                "absent":None,
                "placed":None
                },
                "CT":{
                "total":None,
                "present":None,
                "absent":None,
                "placed":None
                },
                "AIDS":{
                "total":None,
                "present":None,
                "absent":None,
                "placed":None
                },
                "ME":{
                "total":None,
                "present":None,
                "absent":None,
                "placed":None
                },
                "CE":{
                "total":None,
                "present":None,
                "absent":None,
                "placed":None
                },
                "EL":{
                "total":None,
                "present":None,
                "absent":None,
                "placed":None
                },
                "EE":{
                "total":None,
                "present":None,
                "absent":None,
                "placed":None
                },
                "ETC":{
                "total":None,
                "present":None,
                "absent":None,
                "placed":None
                },
                "IIOT":{
                "total":None,
                "present":None,
                "absent":None,
                "placed":None
                },
            })
            c = Campus(name = name,date = date,pack = pack,departments = departments)
            db.session.add(c)
            db.session.commit()
            return redirect("/addCampus")

        return render_template("addcampus.html")
    return  redirect("/login")

@app.route("/download/<string:camp>")
def download(camp):
    user = session.get('user')
    if user and user == 'admin':

        data = Student.query.filter(Student.company == camp).all()
        df = pd.DataFrame([{
            'Name': student.name,
            'Student ID': student.student_id,
            'Department': student.department,
            'Class': student.cls,
            'Phone No': student.phoneno,
            'Email': student.email,
            'Company': student.company,
            'Date': student.date,
            'Hash': student.hash,
            'Attendance': student.attendance,
            'Placed': student.placed
        } for student in data])

        # Save the DataFrame to an Excel file
        file_path = f"{camp}_data.xlsx"
        df.to_excel(file_path, index=False)

        # Send the file as a response
        return send_file(file_path, as_attachment=True, download_name=file_path)
    return  redirect("/login")

    
@app.route("/download/<string:camp>/<string:dept>")
def downloadDept(camp,dept):
    user = session.get('user')
    if user and user == 'admin':
        if dept == 'clg':
            data = Student.query.filter(Student.company == camp).all()
        else:
            data = Student.query.filter(Student.company == camp,Student.department == dept).all()

        
        df = pd.DataFrame([{
            'Name': student.name,
            'Student ID': student.student_id,
            'Department': student.department,
            'Class': student.cls,
            'Phone No': student.phoneno,
            'Email': student.email,
            'Company': student.company,
            'Date': student.date,
            'Hash': student.hash,
            'Attendance': student.attendance,
            'Placed': student.placed
        } for student in data])

        # Save the DataFrame to an Excel file
        file_path = f"{camp}_{dept}_data.xlsx"
        df.to_excel(file_path, index=False)

        # Send the file as a response
        return send_file(file_path, as_attachment=True, download_name=file_path)
    return  redirect("/login")

    


@app.route("/download/<string:camp>/<string:dept>/absent")
def downloadDeptabsent(camp,dept):
    user = session.get('user')
    if user and user == 'admin':

        if dept == 'clg':
            data = Student.query.filter(Student.company == camp,Student.attendance == 'absent').all()
        else:
            data = Student.query.filter(Student.company == camp,Student.department == dept,Student.attendance == 'absent').all()
        df = pd.DataFrame([{
            'Name': student.name,
            'Student ID': student.student_id,
            'Department': student.department,
            'Class': student.cls,
            'Phone No': student.phoneno,
            'Email': student.email,
            'Company': student.company,
            'Date': student.date,
            'Hash': student.hash,
            'Attendance': student.attendance,
            'Placed': student.placed
        } for student in data])

        # Save the DataFrame to an Excel file
        file_path = f"{camp}_{dept}_absent_data.xlsx"
        df.to_excel(file_path, index=False)

        # Send the file as a response
        return send_file(file_path, as_attachment=True, download_name=file_path)
    return  redirect("/login")

  
  
@app.route("/download/<string:camp>/<string:dept>/present")
def downloadDeptpresent(camp,dept):
    user = session.get('user')
    if user and user == 'admin':

        if dept == 'clg':
            data = Student.query.filter(Student.company == camp,Student.attendance == 'present').all()
        else:
            data = Student.query.filter(Student.company == camp,Student.department == dept,Student.attendance == 'present').all()
        df = pd.DataFrame([{
            'Name': student.name,
            'Student ID': student.student_id,
            'Department': student.department,
            'Class': student.cls,
            'Phone No': student.phoneno,
            'Email': student.email,
            'Company': student.company,
            'Date': student.date,
            'Hash': student.hash,
            'Attendance': student.attendance,
            'Placed': student.placed
        } for student in data])

        # Save the DataFrame to an Excel file
        file_path = f"{camp}_{dept}_present_data.xlsx"
        df.to_excel(file_path, index=False)

        # Send the file as a response
        return send_file(file_path, as_attachment=True, download_name=file_path)
    return  redirect("/login")

 
    
@app.route("/archiveCampus/<string:camp>")
def archiveCampus(camp):
    user = session.get('user')
    if user and user == 'admin':
        # Check if the campus exists in the Campus table
        ca = Campus.query.filter(Campus.name == camp).first()

        if ca:
            # Create a new entry in the ArchivedCampus table
            archived_ca = ArchivedCampus(
                name=ca.name,
                departments=ca.departments,
                pack=ca.pack,
                date=ca.date,
                user_id=ca.user_id
            )

            db.session.add(archived_ca)
            db.session.commit()

            # Delete the campus from the Campus table
            db.session.delete(ca)
            db.session.commit()

            return redirect("/")
        else:
            # Handle the case where the campus doesn't exist
            flash("Campus not found", "error")
            return redirect("/")
    return redirect("/login")
       

@app.route("/delete")
def delete():
    # Fetch all Student records
    students = Student.query.all()

    # Loop through the records and delete them one by one
    for student in students:
        db.session.delete(student)

    # Commit the changes to the database
    db.session.commit()

    return "Data Deleted"




@app.route("/login",methods= ['GET','POST'])
def login():
    if request.method == "POST":
        admin = request.form['admin']
        password = request.form['password']

        if admin == "admin" and password == "password":
            session['user'] = admin
            return redirect("/")
        else:
            id = SubAdmin.query.filter(SubAdmin.loginid == admin).first()
            if id == None:
                return redirect("/login")
            elif id.loginid == admin and id.password == password:
                session["user"] = admin
                return redirect("/createCampus")
        
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user",None)
    return redirect("/login")

# ... (your existing code)

@app.route("/cologin",methods = ['GET','POST'])
def cologin():
    print("tis")
    if request.method == "POST":
        data = request.get_json()
        id = data.get("id")
        password = data.get("password")

        user =Coordinator.query.filter_by(loginid=id, password=password).first()
        if user is None:
            print("subadmin")
            user =SubAdmin.query.filter_by(loginid=id, password=password).first()
            if user is None:
                return jsonify({'message': 'Invalid Credentials'})
            else:
                campus = user.campus
                return jsonify({'message': 'True',"campus":campus})
        else:
            campus = user.campus
            return jsonify({'message': 'True',"campus":campus})


@app.route("/updateAttendance/<string:campus>/<string:hash>",methods = ['PUT'])
def upd(campus,hash):
    student = Student.query.filter(Student.company == campus,Student.hash == hash).first()
    print("d")
    print(student.name)
    if student is None:
        return jsonify({"message":"Student not found"})
    else:
        student.attendance = "present"
        student.date = str(datetime.now(indian_timezone))
        db.session.add(student)
        db.session.commit()
        return jsonify({"message":"True","Name":student.name})
    
if __name__ == "__main__":
    app.run(debug=True)  # Run the app in debug mode for detailed error messages



