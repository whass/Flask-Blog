from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort

import os
from sqlalchemy.orm import sessionmaker
from models import User, Post, create_engine
engine = create_engine('sqlite:///dbMyBlog.db', echo=True)
 
app = Flask(__name__)

 
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Hello Boss!"
 
@app.route('/login', methods=['GET','POST'])
def do_admin_login():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route('/add/' , methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        post=Post(request.form['title'], request.form['body'])
	
	Session = sessionmaker(bind=engine)
	s = Session()

        s.add(post)
        s.commit()
        flash('New entry was successfully posted')     
             
    return render_template('add.html')

@app.route('/show/', methods=['POST', 'GET'])
def show():  
  Session = sessionmaker(bind=engine)
  s = Session()
  post = s.query(Post).all()
  return render_template('blog.html', post=post)

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.debug = True
    app.run()

