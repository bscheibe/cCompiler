import os
import subprocess
import random
# from subprocess import check_output
from flask import Flask, render_template, request, send_from_directory, session
from werkzeug import secure_filename
app = Flask(__name__)

# ALLOWED_EXTENSIONS = set(['c'])

# app.secret_key = '6B\n\xd1R\x90\xbb^/\xc0\x8b\x92\xf8\x85\xe2\xf8u{\xf3q3V\x80[''F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  #10 MB Limit

# print os.environ
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER') or '/Users/brentscheibelhut/Documents/Repos/cCompiler/uploads'
app.config['BINARY_FOLDER'] = os.environ.get('BINARY_FOLDER') or '/Users/brentscheibelhut/Documents/Repos/cCompiler/binaries'

BINARY_FOLDER = '/binaries/'

@app.route('/', methods=['GET', 'POST'])
def upload_file():   
    if request.method == 'POST':
        # file = request.files.get('file')
        error = "Error Uploading"
        try:
            code = request.form.get('code')
            srcname = 'source.c'

            # if file and code:
            #     error = "Error must have one or the other"
            # elif (file and allowed_file(file.filename)) or code:
                # if file:
                #     code = file.read()

            # Get secure filename
            filename=secure_filename(srcname)    
            outfile=open(filename,'w');  
            outfile.write(code);  
            outfile.close(); 

            source=filename
            if file:
                source = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            hash = str(random.getrandbits(128))
            cmd = ['gcc', '-Wall', '-o', os.path.join(app.config['BINARY_FOLDER'], hash), source] 
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()

            if os.path.isfile(os.path.join(app.config['BINARY_FOLDER'], hash)):
                filePath = BINARY_FOLDER + hash
            else:
                filePath = "NULL"

            if err:
                return render_template('index.html', hashFile=filePath, cErr=err, code=code)
            else:
                return render_template('index.html', hashFile=filePath, cSuccess=True, code=code)
        except Exception, e:
            error = e.msg
            return render_template('index.html', error=error, code=code)

        # error = "Error: Unallowed file ending"
        # return render_template('index.html', error=error, code=code)
    else:
        session['UID'] = str(random.getrandbits(128))
        return render_template('index.html')

@app.route('/binaries/<filename>')
def binary_file(filename):
    return send_from_directory(app.config['BINARY_FOLDER'],
                               filename)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(debug=True)
