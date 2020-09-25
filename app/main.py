from flask import Flask, render_template, request, redirect, flash, session
import mysql.connector
import os
import time

#This code for mysql database connection
conn = mysql.connector.connect(host="localhost", user="vishal", password="Vkd123@@", database="app")
cursor = conn.cursor()

#Flask code
app = Flask(__name__)
#create key for session
app.secret_key=os.urandom(24)
#Function for rederct home page
@app.route('/home')
def home():

    if 'user_id' in session:
        return render_template('Home.html')
    else:
        return redirect('/')
#logine page
@app.route('/')
def login():
    if 'user_id' in session:
        return redirect('/home')
    else:
        return render_template('Index.html')

#function for check logine validetion
@app.route('/login validetion', methods=['GET','POST'])
def velidetion():
    email = request.form.get('Uname')
    password = request.form.get('Psw')
    
    cursor.execute("SELECT * FROM users WHERE email LIKE '{}' AND password LIKE '{}'".format(email, password))
    users = cursor.fetchall()
    
    if len(users)>0:
        session['user_id']=users[0][1]
        return redirect('/home')
    else:
        flash("incorrect username or password.")
    return redirect('/')

#singup page
@app.route('/singup', methods=['GET', 'POST'])
def singup():
    if 'user_id' in session:
        return redirect('/home')
    else:
        return render_template('Registration.html')
        
#function for add new user
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    email = request.form.get('email')
    psw = request.form.get('pass')
    res = request.form.get('res1')
    cursor.execute("INSERT INTO users(email, password,reason) VALUES(%s, %s, %s)",(email, psw, res))
    conn.commit()
    return redirect('/home')

#logout function
@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')


#for store user in db for chat battun    
@app.route('/btn', methods=['GET', 'POST'])
def btn():
    v = session['user_id']
    sp = v.split("@")[0]
    cursor.execute("INSERT INTO list(name) VALUES('{}')".format(sp))
    conn.commit()
    return redirect ('/chat')
#This is spot function of chat function
@app.route('/vv')
def vv():
    time.sleep(10)
    cursor.execute("SELECT * FROM gp")
    final = cursor.fetchall()
    nm = final[0][1]
    if len(final)>0:
        cursor.execute("DELETE FROM gp WHERE name='{}' LIMIT 1".format(final[0][1]))
        conn.commit()
        return redirect ("https://meet.jit.si/"+nm)
    else:
        time.sleep(10)
        if len(final)>0:
            cursor.execute("DELETE FROM gp WHERE name='{}' LIMIT 1".format(final[0][1]))
            conn.commit()
            return redirect ("https://meet.jit.si/"+nm)
        else:
            return redirect ('/home')
        

#This is chat function
@app.route('/chat')
def chat():
    cursor.execute("SELECT COUNT(*) FROM list")
    count = list(cursor.fetchall())
    if count[0][0] == 2:
        cursor.execute("SELECT name FROM list")
        users1 = cursor.fetchall()
        a = users1[0][0]
        b = users1[1][0]
        var = a+b
        cursor.execute("INSERT INTO gp(name) VALUES('{}')".format(var))
        cursor.execute("DELETE FROM list WHERE name='{}' LIMIT 1".format(a))
        cursor.execute("DELETE FROM list WHERE name='{}' LIMIT 1".format(b))
        conn.commit()
        time.sleep(10)
        return redirect ("https://meet.jit.si/"+var)
    else:
        return redirect ('/vv')
    

#code for updae app withot restart app
if __name__ == "__main__":
    app.run(debug=True)


