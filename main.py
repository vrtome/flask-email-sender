from distutils.log import debug
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for, jsonify, flash
import send_email as se
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/response')
def response():
    print("got to response")
    return render_template('response.html')


@app.route("/")
@app.route('/email', methods=['POST', 'GET'])
def email():
    if request.method == 'POST':
        addr = request.remote_addr
        print("rawrr")
        print(request.form)
        emailHead = request.form['subject']
        hmmhead = "head: " + emailHead
        print(hmmhead)

        emailBody = request.form['text']
        hmmbody = "body: " + emailBody
        print(hmmbody)

        emailSender = request.form['sender']
        hmmsender = "sender: " + emailSender
        print(hmmsender)

        emailRecipient = request.form['recipient']
        hmmrecipient = "recipient: " + emailRecipient
        print(hmmrecipient)

        emailPassword = request.form['password']
        hmmpassword = "password: " + emailPassword
        print(hmmpassword)

        # check if the post request has the file part
        if 'upload' not in request.files:
            flash('No file part')
            #return redirect(request.url)
        file = request.files['upload']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            #return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return redirect(url_for('download_file', name=filename))
        emailUpload = filename  #request.form['upload']
        hmmupload = "upload: " + emailUpload
        print(hmmupload)

        print(type(emailUpload))
        se.send_email(emailHead, emailBody, emailSender, emailRecipient,
                      emailPassword, emailUpload)
        print("got out of email")
        return redirect(url_for('response'))
    else:
        print("chwddd")
        emailHead = request.args.get('subject')
        emailBody = request.args.get('text')

        return render_template('email.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")
