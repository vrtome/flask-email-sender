from distutils.log import debug
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for, jsonify
import send_email as se

app = Flask(__name__)


@app.route('/response')
def response():
    return render_template('response.html')


@app.route("/")
@app.route('/email', methods=['POST', 'GET'])
def email():
    if request.method == 'POST':
        addr = request.remote_addr
        print("rawrr")
        print(addr)
        emailHead = request.form['subject']
        print(emailHead)
        emailBody = request.form['text']
        emailSender = request.form['sender']
        emailRecipient = request.form['recipient']
        emailPassword = request.form['password']
        emailUpload = request.form['upload']
        print(type(emailUpload))
        se.send_email(emailHead, emailBody, emailSender, emailRecipient,
                      emailPassword, emailUpload)
        return redirect(url_for('response'))
    else:
        emailHead = request.args.get('subject')
        emailBody = request.args.get('text')
        render_template('email.html')
        return redirect(url_for('response'))


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")
