from flask import Flask, url_for, render_template, request
app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

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

if __name__ == '__main__':
    app.run(debug=True)
