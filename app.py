import time
from flask import render_template,request,redirect,Flask
from werkzeug.utils import secure_filename
import os

ALLOW_EXTENSIONS = {'gz','tar.gz'}
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.config['Max_CONTENT_LENGTH']=400*1024*1024

def allow_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOW_EXTENSIONS


@app.route('/',methods=['POST','GET'])
def welcome():
    return render_template('index.html',show_app="home")

@app.route('/show',methods=['POST','GET'])
def submit():
    return render_template('index.html',show_app="add")

@app.route('/add',methods=['POST','GET'])
def add():
    start=time.time()
    if 'file' not in request.files:
        print('no file attached')
        return redirect('/show')
    file = request.files['file']
    if file.filename == '':
        print('no file select')
        return redirect('/show')
    if file and allow_file(file.filename):
        filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
    path = (os.path.join(app.config['UPLOAD_FOLDER'],filename))
    print("path:",path)
    print(time.time()-start)
    return redirect('/')

if __name__ == "__main__":
        app.run()