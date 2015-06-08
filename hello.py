import os
import subprocess
import random
from flask import Flask, render_template, request, send_from_directory, session
from werkzeug import secure_filename
# from werkzeug.contrib.securecookie import SecureCookie
app = Flask(__name__)

# ALLOWED_EXTENSIONS = set(['c'])

#10 MB Limit for requests
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 

# Holds user uploads
# app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER') or './uploads'
app.config['BINARY_FOLDER'] = os.environ.get('BINARY_FOLDER') or './binaries/'

# Secret key - line long but not liking '/' to split
app.secret_key = os.environ.get('SECRET_KEY') or '6B\n\xd1R\x90\xbb^/\xc0\x8b\x92\xf8\x85\xe2\xf8u{\xf3q3V\x80[''F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'

@app.route('/', methods=['GET', 'POST'])
def upload_file():  
    
    #Should have some notification to user on invalid cookie
    if request.method == 'POST' and session.get('UID'):
        # file = request.files.get('file')

        #Source file name
        srcname = 'source.c'

        #Get user's code from form
        code = request.form.get('code')

        #Where the users binary was stored
        filePath = 'NULL'

        try:
            

            #----- Keeping to allow for file uploads in the future ---#
            # if file and code:
            #     error = "Error must have one or the other"
            # elif (file and allowed_file(file.filename)) or code:
                # if file:
                #     code = file.read()
            #--- Keeping for future use ---#


            # Get secure filename and write to tempfile
            filename=secure_filename(srcname)    
            outfile=open(filename,'w');  
            outfile.write(code);  
            outfile.close(); 

            # Compile binary and store in hashed file
            hash = str(random.getrandbits(128))
            cmd = ['gcc', '-Wall', '-o', os.path.join(app.config['BINARY_FOLDER'], hash), filename] 
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()

            #Check if a binary file was generated and set template var
            if os.path.isfile(os.path.join(app.config['BINARY_FOLDER'], hash)):
                filePath = app.config['BINARY_FOLDER'] + hash

            #If no errors still set to NULL so template knows to render binary side
            err = err or 'NULL'
            return render_template('index.html', hashFile=filePath, cErr=err, code=code,)
        except Exception, e:
            #Keep users code and alert of error message
            err = str(e) or "Error Uploading. Please try again."
            return render_template('index.html', hashFile=filePath, cErr=err, code=code)

        #---- Keeping to use when accepting file uploading ---#
        # error = "Error: Unallowed file ending"
        # return render_template('index.html', error=error, code=code)
    else:
        session['UID'] = str(random.getrandbits(128))
        return render_template('index.html')

#Allows for downloading of the binary
@app.route('/binaries/<filename>')
def binary_file(filename):
    return send_from_directory(app.config['BINARY_FOLDER'],
                               filename,
                                as_attachment=True,
                                attachment_filename="output")

#Handles four-oh-four errors
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

#---- Keeping for when I allow file uploading ---#
# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
#----Keeping for when I allow file uploading ---#

if __name__ == '__main__':
    app.run(debug=True)
