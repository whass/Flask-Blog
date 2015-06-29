from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from sqlalchemy.orm import sessionmaker
from models import User, Post, create_engine, Category
from datetime import datetime
from flask_frozen import Freezer

engine = create_engine('sqlite:///dbMyBlog.db', echo=True)

freezer = Freezer(app)
app = Flask(__name__,  static_url_path='')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/hire')
def hire():
    return render_template('hire.html')
 
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
    	Session = sessionmaker(bind=engine)
    	s = Session()
    	query = s.query(User).filter(User.username.in_('username'), User.password.in_('password') )
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
    Session = sessionmaker(bind=engine)
    s = Session()
    categories = s.query(Category).all()

    if not session.get('logged_in'):
        return render_template('login.html')

    if (request.method == 'POST'):	
        post=Post(request.form['title'], request.form['description'], request.form['body'], request.form['category_id'])
	s.add(post)
        s.commit()
    return render_template('add.html', categories=categories)	

@app.route('/update/<int:post_id>' , methods=['POST', 'GET'])
def update(post_id):
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        Session = sessionmaker(bind=engine)
        s = Session()
        categories = s.query(Category).all()
        post=s.query(Post).get(post_id)
        if (request.method == 'POST'):
             s.query(Post).filter_by(id=post_id).update({"title": request.form['title'], "description": request.form['description'], "body": request.form['body'], "category_id":request.form['category_id'], "updated_at": datetime.utcnow()})
             s.commit()
    return render_template('update.html', post=post, categories=categories)	

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
 
@app.route('/posts/', methods=['POST', 'GET'])
def posts():  
    Session = sessionmaker(bind=engine)
    s = Session()
    post = s.query(Post).all()
    category = s.query(Category).all()
    return render_template('posts.html', post=post, category=category)

@app.route('/post/<int:post_id>')
def post(post_id):  
    Session = sessionmaker(bind=engine)
    s = Session()
    post = s.query(Post).get(post_id)
    posts = s.query(Post).all()
    return render_template('post.html', post=post, posts=posts)


@app.route('/add_category/' , methods=['POST', 'GET'])
def add_category():
    if not session.get('logged_in'):
        return render_template('login.html')

    if (request.method == 'POST'):
        category=Category(request.form['name'])
	
	Session = sessionmaker(bind=engine)
	s = Session()

	s.add(category)
        s.commit()
    return render_template('add_category.html')	

@app.route('/update_category/<int:category_id>' , methods=['POST', 'GET'])
def update_category(category_id):
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        Session = sessionmaker(bind=engine)
        s = Session()
        category=s.query(Category).get(category_id)
        if (request.method == 'POST'):
             category1=Category(request.form['name'])
             s.query(Category).filter_by(id=category_id).update({"name": category1.name})
             s.commit()	
        return render_template('update_category.html', category=category)	

@app.route('/delete_category/<int:category_id>')
def delete_category(category_id):  
    if not session.get('logged_in'):
        return render_template('login.html')
 
    else: 
	Session = sessionmaker(bind=engine)
        s = Session()
        category = s.query(Category).get(category_id)
        s.delete(category) 
        s.commit()
        return "deleted"
 
@app.route('/categories/', methods=['POST', 'GET'])
def categories():  
    Session = sessionmaker(bind=engine)
    s = Session()
    categories = s.query(Category).all()
    return render_template('categories.html', categories=categories)

@app.route('/category/<int:category_id>')
def category(category_id):  
    Session = sessionmaker(bind=engine)
    s = Session()
    category = s.query(Category).get(category_id)
    return render_template('category.html', category=category)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(debug=True)	
        app.secret_key = os.urandom(12)
        app.debug = True
        app.run()
