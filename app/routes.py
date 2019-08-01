from app import app
from flask import render_template, request, redirect, session, url_for
from app.models import model, formopener
from flask_pymongo import PyMongo

#secret key for session
app.secret_key = "anysecretstring"
# name of database
app.config['MONGO_DBNAME'] = 'room_aestheticizer' 
# URI of database
app.config['MONGO_URI'] = 'mongodb+srv://crystalyang:crystal123@cluster0-xrzh9.mongodb.net/room_aestheticizer?retryWrites=true&w=majority'

mongo = PyMongo(app)

@app.route('/')
@app.route('/index')
def index():
    if 'username' not in session:
        nameDisplay = "New User"
    else:
        nameDisplay = session['username']
    return render_template('index.html', nameDisplay = nameDisplay)
    
@app.route('/results', methods = ['GET', 'POST'])
def results():
    if request.method == 'GET':
        return "You're getting the furniture page. Please return to the form!"
    else:
        userdata = dict(request.form)
        room_type =(userdata['room_type'])
        furniture =(userdata['furniture'])
        color =(userdata['color'])
        URL = model.IkeaURLs(furniture, color)
        URL1 = model.MacysURLs(furniture, color)
        URL2 = model.RaysURLs(furniture, color)
        print(URL)
        print(URL1)
        print(URL2)
        print(userdata)
        error = model.options(room_type, furniture)
        print(error)
        if error == False:
            return render_template('error.html')
        else:
            
        # ikea = model.IkeaURLs(room_type, furniture, color, URL)
        # print(ikea)
            return render_template('results.html', room_type = room_type, furniture = furniture, color = color, URL = URL, URL1 = URL1, URL2 = URL2, error = error )
@app.route('/signup', methods=['POST','GET'])
def signup():
    if 'username' not in session:
        session['username'] = 'new user'
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name': request.form['username']})
        
        if existing_user is None:
            users.insert({'name': request.form['username'], 'password': request.form['password']})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        else:
            return 'That username already exists!  Try logging in.'
    nameDisplay = session['username']
    return render_template('signup.html', nameDisplay = nameDisplay)
    
@app.route('/login', methods=['GET','POST'])
def login():
    if 'username' not in session:
        return render_template('login.html')
   
    elif request.method == 'POST':
        users = mongo.db.users
        login_data = dict(request.form)
        login_user = users.find_one({'name' : login_data['username']})
        if login_user:
            if login_data['password'] == login_user['password']:
                session['username'] = login_data['username']
                return redirect('/index')
        return 'Invalid username/password combination'
        
    else:
        nameDisplay = session['username']
        return render_template('login.html', nameDisplay = nameDisplay)
            
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

        
        
        