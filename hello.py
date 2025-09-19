from flask import Flask, make_response, redirect, abort, current_app, request,g,render_template

app = Flask(__name__)

@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    return '<p>Your browser is {}</p>'.format(user_agent)

@app.route('/massage')
def massage():
    # بيانات تجريبية
    comments = ["Nice post!", "Thanks for sharing.", "Very helpful.", "Awesome!"]
    user = None
    return render_template('index.html', user=user, comments=comments)

@app.route('/appname')
def app_name():
    return '<h1>App Name: {}</h1>'.format(current_app.name)

@app.route('/response')
def response():
    return '<h1>Normal Response</h1>'

@app.route('/cookie')
def cookie():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer', '42')
    return response

@app.route('/redirect')
def go_google():
    return redirect('http://www.google.com')

@app.route('/error')
def error():
    abort(404)
    
@app.before_request
def before_request():
    g.message = "Hello from before_request!"
    
@app.before_request
def before_request():
    g.message = "Hello from before_request!"


@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)





@app.route('/variables')
def variables():
    # Dictionary
    mydict = {"fruit": "Mango"}

    # List
    mylist = ["Math", "Science", "History"]

    # Index
    myindex = 1  # يعني حيجيب العنصر الثاني من القائمة

    # Object
    class Teacher:
        def somemethod(self):
            return "Study hard and be consistent!"
    myobj = Teacher()

    # HTML محتوى
    html_content = "<b>This text is bold</b>"

    return render_template(
        'variables.html',
        mydict=mydict,
        mylist=mylist,
        myindex=myindex,
        myobj=myobj,
        html_content=html_content
    )






if __name__ == '__main__':
    app.run(debug=True)
