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

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    # file = request.files['file']
    # if file and allowed_file(file.filename):
    #     filename = secure_filename(file.filename)
    #     print "cool"
    #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #     return redirect(url_for('uploaded_file',
    #                             filename=filename))

    if request.method == 'POST':
        file = request.files.get('file')
        code = request.form.get('code')
        srcname = 'source.c'
        error = "Error Uploading"

        if file and code:
            error = "Error must have one or the other"
        elif file or code:
            if allowed_file(srcname):
                if file:
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                elif code:
                    if allowed_file(srcname):
                        outfile=open(srcname,'w');  
                        outfile.write(code);  
                        outfile.close(); 

                # return redirect(url_for('uploaded_file', filename=filename))
                source=srcname
                if file:
                    source = os.path.join(app.config['UPLOAD_FOLDER'], srcname)

                cmd = ['gcc', '-Wall', '-o', os.path.join(app.config['BINARY_FOLDER'], 'output'), source] 
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = p.communicate()

                print "Output: " + out
                print "Errors or Warning: " + err

                # flash(err)
                # Need hased filename to return
                return render_template('index.html', cErr=err, code=code)
            else:
                error = "Error: Unallowed filename"

            #return render_template('upload.html', output=err)

        return render_template('index.html', error=error, code=code)
    else: 
        return render_template('index.html')
    #subprocess.call(["./"+execname]);  

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/binaries/<filename>')
def binary_file(filename):
    return send_from_directory(app.config['BINARY_FOLDER'],
                               filename)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(debug=True)
