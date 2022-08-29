from flask import Flask, request, url_for, current_app
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

app = Flask(__name__)
app.config.from_pyfile('config1.py')

mail = Mail(app)

s = URLSafeTimedSerializer('Thisisasecret!')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return '<form action="/" method="POST"><input name="email"><input type="submit"></form>'

    '''email = 'roxep82842@otodir.com'
    token = s.dumps('roxep82842@otodir.com')'''

    msg = Message('Confirm Email', sender='someone@gmail.com', recipients=['roxep82842@otodir.com'])

    #link = url_for('confirm_email', token=token, _external=True)

    msg.body = 'Your link is {}'.format(link)

    mail.send(msg)

    #return '<h1>The email you entered is {}. The token is {}</h1>'.format(email, token)

@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except SignatureExpired:
        return '<h1>The token is expired!</h1>'
    return '<h1>The token works!</h1>'

if __name__ == '__main__':
    app.run(debug=True)