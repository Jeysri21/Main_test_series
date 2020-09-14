from flask import Flask,render_template,flash,url_for,redirect,session,logging,request
from passlib.hash import sha256_crypt
import mysql.connector
from functools import wraps
import time
import pandas as pd
import os
from csv import writer
import random
from datetime import datetime


app=Flask(__name__)

#Config Mysql
mydb=mysql.connector.connect(host='localhost',user="root",passwd="",database="blogdb")

data=pd.read_csv('bm.csv')
records=data.to_records(index=False)
result = list(records)
q1=random.choice(result)
q2=random.choice(result)
coding=pd.read_csv('coding.csv')
coding_records=coding.to_records(index=False)
code_result = list(coding_records)
q3=random.choice(code_result)
q4=random.choice(code_result)
current=pd.read_csv('ca.csv')
current_records=current.to_records(index=False)
current_result = list(current_records)
q5=random.choice(current_result)
q6=random.choice(current_result)


# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap


#Homepage
@app.route('/')
def home():
    return render_template('homepage1.html')

#Registration
@app.route('/register' ,methods=['GET','POST'])
def register():
    # form=RegisterForm()
    # profile = request.files['img']
    if request.method=='POST':
        image = request.files['img']
        name=request.form.get('name')
        lname=request.form.get('fname')
        email=request.form.get('email')
        username=request.form.get('username')
        password=request.form.get('password')
        usn=request.form.get('usn')
        gender=request.form.get('gender')
        depart=request.form.get('depart')
        phone=request.form.get('phone')
        filename = username + ".jpg"
        filename = os.path.join('static/images/profile/',filename)
        image.save(filename)
        # Creating Cursor
        cur=mydb.cursor()
        
        cur.execute("INSERT INTO dsc(name,lname,email,username,password,usn,gender,depart,phone) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s )",(name,lname,email,username,password,usn,gender,depart,phone))
        
        #Commit to db
        mydb.commit()
        
        #close Connection
        cur.close()
        
        flash("Successfully registered","success")
        
        redirect('/index')
        # return form.email.data
        return redirect('/login')
    return render_template('registration.html')

#Login page
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        #Geeting the form field
        username=request.form.get('username')
        password_candidate=request.form.get('password')
        
        #Create Cursor
        cur=mydb.cursor(buffered=True)

        #Get user by username
        
        result=cur.execute("select * from dsc where username = %s",[username])
        
        if result == None:
            #Getting the stored hashed
            data=cur.fetchone()
            password=data[4]
            #Comparing the password
            if password_candidate==password:
                session['logged_in']=True
                session['username']=username
                flash("Congrats you are logged in")
                return redirect('/dashboard')
                app.logger.info('Password Matched')
                
            else:
                app.logger.info("Password not matched")
                error="Invalid login"
                flash("password not matched")
                return render_template('logins.html',error=error)
            #Close connection
            cur.close()
        else:
            app.logger.info("No User")
            flash("No user found")
            return render_template('logins.html',error=error)
    return render_template('logins.html')


#Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    name=session['username']
    cur=mydb.cursor()
    cur.execute("SELECT * FROM dsc WHERE username = %s", [name])
    information=cur.fetchall()
    return render_template('dashboard.html',name=name,info=information)

#Team
@app.route('/team')
def team():
    return render_template('team.html')

#Test_portal
@app.route('/test')
@is_logged_in
def test():  
        # with open('answer.csv', 'a+', newline='') as write_obj:
        #     csv_writer = writer(write_obj)
        #     csv_writer.writerow(ours)
   
    return render_template('quiz2.html',name="poorna",q1=q1,q2=q2,q3=q3,q4=q4,q5=q5,q6=q6,q7=q4,q8=q4,q9=q4,q10=q4)
    
    
    
@app.route('/answer',methods=['GET','POST'])
@is_logged_in
def answer():
    if request.method == "POST":
        qes1=request.form.get('q1')
        qes2=request.form.get('q2')
        qes3=request.form.get('q3')
        qes4=request.form.get('q4')
        qes5=request.form.get('q5')
        qes6=request.form.get('q6')
        qes7=request.form.get('q7')
        qes8=request.form.get('q8')
        qes9=request.form.get('q9')
        qes10=request.form.get('q10')
        points=0
        if (q1[6]==qes1):
            points=points+10
        if (q2[6]==qes2):
            points=points+10
        if (q3[6]==qes3):
            points=points+10
        if (q4[6]==qes4):
            points=points+10
        if (q1[6]==qes1):
            points=points+10
        if (q1[6]==qes1):
            points=points+10
        if (q1[6]==qes1):
            points=points+10
        if (q1[6]==qes1):
            points=points+10
        if (q1[6]==qes1):
            points=points+10
        if (q1[6]==qes1):
            points=points+10
        if (q1[6]==qes1):
            points=points+10
        
        name=session['username']
        points = str(points)
        with open('answer.csv','r+') as f:
            myDataList=f.readlines()
            nameList=[]
            for line in myDataList:
                entry = line.split(',') 
                nameList.append('added') 
            
            if name not in nameList:
                now =datetime.now()
                dtString=now.strftime('%H:%M:%S')
                f.writelines(f'\n{name},{dtString},{points}')
            
        
        return redirect('/score')
    return "Not working yet"

#Result
@app.route('/score')
@is_logged_in
def score():
    score=pd.read_csv('answer.csv')
    score1=score.to_records(index=False)
    result = list(score1)
    # lists1 = list.sort_values("marks", ascending=True)
    return render_template('score.html',results=result)

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('homepage.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('homepage.html'), 500

#Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash("Successfully Logged out!!!")
    return redirect('/login')


if __name__=="__main__":
    app.secret_key='poorna1999'
    app.run(debug=True)