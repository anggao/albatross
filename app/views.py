from flask import render_template, request, g
from app import app, config
from app import models

from werkzeug.contrib.atom import AtomFeed

@app.template_filter('date')
def format_date(value, format="%B %d, %Y"):
    return value.strftime(format)

@app.before_request
def preconfig():
    g.config = config

@app.route('/')
def index():
    return render_template('index.html', posts=models.blog.posts)

@app.route('/blog/<path:path>/')
def post(path):
    post = models.Post(path+app.config['POSTS_FILE_EXTENSION'], root_dir='posts')
    return render_template('post.html', post=post)

@app.route('/tags/')
def tags():
    return render_template('tags.html', tags=models.blog.get_posts_with_tag)

@app.route('/achive/')
def achive():
    return render_template('achive.html', posts=models.blog.posts)

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/feed.atom')
def feed():
    feed = AtomFeed('Recent Posts',
            feed_url = request.url,
            url = request.url_root)
    posts = models.blog.posts[:10]
    title = lambda p: '%s : %s' % (p.title, p.subtitle) if hasattr(p,
            'subtitle') else p.title
    for post in posts:
        feed.add(title(post),
            unicode(post.html),
            content_type='html',
            author='Ang Gao',
            url = post.url(_external=True),
            updated=post.date,
            published=post.date)
    return feed.get_response()
