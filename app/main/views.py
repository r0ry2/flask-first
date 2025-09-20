# app/main/views.py
from datetime import datetime
from flask import render_template, session, redirect, url_for, request, flash
from . import main
from .forms import NameForm
from datetime import datetime
from .. import db
from ..models import User

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    comments = ["Nice app!", "Great work!"]

    if form.validate_on_submit():
        name = form.name.data
        user = User.query.filter_by(username=name).first()
        if user is None:
            user = User(username=name)
            db.session.add(user)
            db.session.commit()
            flash("New user added to database!")
        else:
            flash("Welcome back!")

        session['name'] = name
        return redirect(url_for('.index'))

    return render_template(
        'index.html',
        user=session.get('name'),
        current_time=datetime.utcnow(),
        user_agent=request.headers.get('User-Agent'),
        form=form,
        comments=comments
    )
    
    

# صفحة مستخدم /user/<name>
@main.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

# صفحة variables (نقلنا مثال variables.html)
@main.route('/variables')
def variables():
    mydict = {'fruit': 'Apple'}
    mylist = ['Math', 'Science', 'History']
    myindex = 1
    class MyObj:
        def somemethod(self):
            return "Hello from method!"
    myobj = MyObj()
    html_content = "<b>This is bold HTML text</b>"

    return render_template(
        'variables.html',
        mydict=mydict,
        mylist=mylist,
        myindex=myindex,
        myobj=myobj,
        html_content=html_content
    )
