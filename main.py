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
        print(addr)
        emailHead = request.form.get['subject']
        emailBody = request.form['text']
        emailSender = request.form.get['sender']
        emailRecipient = request.form.get['recipient']
        emailPassword = request.form.get['password']
        emailUpload = request.form.get['upload']
        print(type(emailUpload))
        se.send_email(emailHead, emailBody, emailSender, emailRecipient,
                      emailPassword, emailUpload)
        redirect(url_for('response'))
        return jsonify(result={"status": 200})
    else:
        emailHead = request.args.get('subject')
        emailBody = request.args.get('text')
        render_template('email.html')
        return jsonify(result={"status": 200})


if __name__ == '__main__':
    app.run(debug=True)
