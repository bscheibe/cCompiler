import os
import subprocess
# from subprocess import check_output
from flask import Flask, url_for, render_template, request, send_from_directory, \
	redirect, session, escape, flash
from werkzeug import secure_filename
app = Flask(__name__)

# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
ALLOWED_EXTENSIONS = set(['c'])

# print os.environ
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER') or '/Users/brentscheibelhut/Documents/Repos/cCompiler/uploads'
app.config['BINARY_FOLDER'] = os.environ.get('BINARY_FOLDER') or '/Users/brentscheibelhut/Documents/Repos/cCompiler/binaries'

@app.route('/uploadC', methods=['POST'])
def upload_file():
    # file = request.files['file']
    # if file and allowed_file(file.filename):
    #     filename = secure_filename(file.filename)
    #     print "cool"
    #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #     return redirect(url_for('uploaded_file',
    #                             filename=filename))

    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Might not need to save
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # return redirect(url_for('uploaded_file', filename=filename))
        cmd = ['gcc', '-Wall', '-o', os.path.join(app.config['BINARY_FOLDER'], 'output'), os.path.join(app.config['UPLOAD_FOLDER'], filename)] 
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # out = check_output(cmd)
        # probs don't need, communicate doesn't run until done
        # p.wait();
        # out, err = p.communicate()
        out, err = p.communicate()

        print "Output: " + out
        print "Errors or Warning: " + err

        return render_template('upload.html', output=err)
    return "Error uploading"

    #subprocess.call(["./"+execname]);  

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/binaries/<filename>')
def binary_file(filename):
    return send_from_directory(app.config['BINARY_FOLDER'],
                               filename)

@app.route('/')
def hello():
	return render_template('index.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(debug=True)
