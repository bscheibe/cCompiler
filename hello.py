import os
from flask import Flask, url_for, render_template, request, send_from_directory, redirect
from werkzeug import secure_filename
app = Flask(__name__)

UPLOAD_FOLDER = '/Users/schybo/Documents/Repos/Apps/FlaskApp/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print "cool"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return 

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

"""@app.route('/')
def index():
    return 'Index Page'"""

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

with app.test_request_context():
	print url_for('static', filename='style.css')

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name="Brent"):
    return render_template('hello.html', name=name)

with app.test_request_context('/cool', method='POST'):
    # now you can do something with the request until the
    # end of the with block, such as basic assertions:
    assert request.path == '/cool'
    assert request.method == 'POST'

"""@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['cool.txt']
        f.save('/var/www/uploads/uploaded_file.txt')"""

if __name__ == '__main__':
    app.run(debug=True)
