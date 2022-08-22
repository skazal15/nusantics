import time
from flask import render_template,request,redirect,Flask
import sys
from werkzeug.utils import secure_filename
import os
from io import StringIO

ALLOW_EXTENSIONS = {'gz','tar.gz'}
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.config['CHUNK_SIZE'] = 4096
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
    path = os.path.join(app.config['UPLOAD_FOLDER'],filename)
    chunk_size = app.config['CHUNK_SIZE']
    try:
        with open(path, "wb") as f:
            reached_end = False
            while not reached_end:
                chunk = request.stream.read(chunk_size)
                if len(chunk) == 0:
                    reached_end = True
                else:
                    sys.stdout.write(".")
                    sys.stdout.flush()
                    # the idea behind this chunked upload is that large content could be persisted
                    # somewhere besides the container: S3, NFS, etc...
                    # So we use a container with minimal mem/disk, that can handle large files
                    #
                    #f.write(chunk)
                    #f.flush()
                    #print("wrote chunk of {}".format(len(chunk)))
    except OSError as e:
        print("ERROR writing file " + filename + " to disk: " + StringIO(str(e)).getvalue())
        return redirect('/')

    print("SUCCESS uploading single file: " + filename)
    print("path:",path)
    print(time.time()-start)
    return redirect('/')

if __name__ == "__main__":
        app.run()