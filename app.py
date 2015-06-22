from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from sqlalchemy.orm import sessionmaker
from models import User, Post, create_engine
from datetime import datetime

engine = create_engine('sqlite:///dbMyBlog.db', echo=True)
 
app = Flask(__name__,  static_url_path='')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/')
def home():
    Session = sessionmaker(bind=engine)
    s = Session()
    post = s.query(Post).all()
    return render_template('index.html', post=post)

 
@app.route('/login', methods=['GET','POST'])
def login():
    if session.get('logged_in'):
        return "your are logged already"

    if request.method == 'POST':
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
    return render_template('login.html')

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route('/add/' , methods=['POST', 'GET'])
def add():
    if not session.get('logged_in'):
        return render_template('login.html')

    if (request.method == 'POST'):
        post=Post(request.form['title'], request.form['body'])
	
	Session = sessionmaker(bind=engine)
	s = Session()

	s.add(post)
        s.commit()
    return render_template('add.html')	

@app.route('/update/<int:post_id>' , methods=['POST', 'GET'])
def update(post_id):
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        Session = sessionmaker(bind=engine)
        s = Session()
        post=s.query(Post).get(post_id)
        if (request.method == 'POST'):
             post1=Post(request.form['title'], request.form['body'])
             s.query(Post).filter_by(id=post_id).update({"title": post1.title, "body": post1.body, "updated_at": datetime.utcnow()})
             s.commit()	
        return render_template('update.html', post=post)	

@app.route('/delete/<int:post_id>')
def delete(post_id):  
    if not session.get('logged_in'):
        return render_template('login.html')
 
    else: 
	Session = sessionmaker(bind=engine)
        s = Session()
        post = s.query(Post).get(post_id)
        s.delete(post) 
        s.commit()
        return "deleted"
 
@app.route('/show/', methods=['POST', 'GET'])
def show():  
    Session = sessionmaker(bind=engine)
    s = Session()
    post = s.query(Post).all()
    return render_template('blog.html', post=post)

@app.route('/show/<int:post_id>')
def show_single(post_id):  
    Session = sessionmaker(bind=engine)
    s = Session()
    post = s.query(Post).get(post_id)
    return render_template('blog_single.html', post=post)


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.debug = True
    app.run()

