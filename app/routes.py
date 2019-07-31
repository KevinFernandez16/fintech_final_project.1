from app import app
from flask import render_template, request
from app.models import model, formopener

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
    
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
        
        
        