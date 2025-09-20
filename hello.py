# hello.py (مُحدَّث) — إضافة إرسال إيميل
import os
from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime
from flask import make_response, g, current_app

# ------------------ imports للبريد ------------------
from threading import Thread
from flask_mail import Mail, Message

# ---------------------------------------------------

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

# --- إعدادات البريد (اقرأ من متغيرات البيئة) ---
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'localhost')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT',3000))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'false').lower() in ('true','1','t','yes')
app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL', 'false').lower() in ('true','1','t','yes')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')  # يمكن أن يكون None للاختبار المحلي
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = os.environ.get('FLASKY_MAIL_SUBJECT_PREFIX', '[Flasky] ')
app.config['FLASKY_MAIL_SENDER'] = os.environ.get('FLASKY_MAIL_SENDER', 'Flasky Admin <flasky@example.com>')
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')  # البريد الذي سيستقبل الإشعارات

mail = Mail(app)  # تهيئة Flask-Mail

# ------------------ دوال إرسال الإيميل ------------------
def _send_async_email(app, msg):
    """وظيفة تُشغّل في ثريد وتضمن وجود app_context داخل الثريد."""
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    """بناء الرسالة من قوالب text/html ثم إرسالها في ثريد (غير متزامن)."""
    app = current_app._get_current_object()
    msg = Message(app.config.get('FLASKY_MAIL_SUBJECT_PREFIX', '') + subject,
                  sender=app.config.get('FLASKY_MAIL_SENDER'),
                  recipients=[to])
    # قوالب: template + '.txt' و template + '.html'
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=_send_async_email, args=(app, msg))
    thr.start()
    return thr
# ------------------------------------------------------

bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()  # إنشاء الفورم
    user_agent = request.headers.get('User-Agent')  # متصفح المستخدم

    if form.validate_on_submit():  # تحقق إذا ضغط المستخدم Submit وكانت البيانات صحيحة
        old_name = session.get('name')

        if old_name and old_name != form.name.data:
            flash('Looks like you have changed your name!')  # رسالة فلاش إذا غيّر الاسم
            # إرسال إشعار للمسؤول
            admin = app.config.get('FLASKY_ADMIN')
            if admin:
                send_email(
                    admin,
                    'User changed name',
                    'mail/new_user',
                    user={'username': form.name.data},
                    old_name=old_name
                )
        else:
            # مستخدم جديد (ما كان فيه اسم في الجلسة)
            if not old_name:
                admin = app.config.get('FLASKY_ADMIN')
                if admin:
                    send_email(
                        admin,
                        'New User',
                        'mail/new_user',
                        user={'username': form.name.data}
                    )

        # حفظ الاسم الجديد في الجلسة
        session['name'] = form.name.data
        return redirect(url_for('index'))  # إعادة تحميل الصفحة

    # عرض الصفحة إذا لم يتم الإرسال أو البيانات غير صحيحة
    return render_template(
        'index.html',
        form=form,
        user=session.get('name'),
        current_time=datetime.utcnow(),
        comments=['Welcome!', 'Enjoy your visit!'],
        user_agent=user_agent
    )

    

# ... بقية طرقك دون تغيير ...
@app.route('/time')
def time():
    return render_template(
        'index.html',
        user=None,
        comments=['Great!', 'Nice work'],
        current_time=datetime.utcnow()
    )

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

@app.before_request
def before_request():
    g.message = "Hello from before_request!"

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

# Custom 404 page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Custom 500 page
@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

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
    app.run(debug=True, use_reloader=False, port=5001)
