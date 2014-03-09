from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return 'hello world'

@app.route('/blog/post/')
def post():
    return render_template('post.html', post_content = 'Hello world !')
if __name__ == '__main__':
    app.run(port=8000)
