import os
import markdown
import yaml
import sys
import collections

from flask import Flask, render_template, url_for, abort
from flask import request
from flask.ext.frozen import Freezer
from werkzeug import cached_property
from werkzeug.contrib.atom import AtomFeed

class SortedDict(collections.MutableMapping):
    def __init__(self, items = None, key = None, reverse = False):
        self._items = {}
        self._keys = []
        if key:
            self._key_fun = lambda x : key(self._items[x])
        else:
            self._key_fun = lambda x : self._items[x]
        self._reverse = reverse
        if items is not None:
            self.update(items)

    def __getitem__(self, key):
        return self._items[key]

    def __len__(self):
        return len(self._keys)

    def __iter__(self):
        for k in self._keys:
            yield k

    def __delitem__(self, key):
        self._items.pop(key)
        self._keys.remove(key)

    def __setitem__(self, key, value):
        self._items[key] = value
        if key not in self._keys:
            self._keys.append(key)
            self._keys.sort(key=self._key_fun, reverse=self._reverse)

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self._items)


class Blog:
    def __init__(self, app, root_dir, file_ext = None):
        self._app = app
        self.root_dir = root_dir
        self.ext = file_ext if file_ext is not None else app.config['POSTS_FILE_EXTENSION']
        self._cache = SortedDict(key=lambda p: p.date, reverse=True)
        self._initialize_cache()

    def _initialize_cache(self):
        """Walks the root directory and adds all posts to the cache
        """
        for dirpath, dirnames, filenames in os.walk(self.root_dir):
            for filename in filenames:
                if os.path.splitext(filename)[1] == self.ext:
                    post = Post(filename, 'posts')
                    self._cache[post.urlpath] = post

    @property
    def posts(self):
        if self._app.debug:
            return self._cache.values()
        else:
            return [post for post in self._cache.values() if post.published]

    def get_post_or_404(self, path):
        """Returns the Post object for the given path or raises an NotFound
        exception
        """
        try:
            return self._cache[path]
        except KeyError:
            abort(404)

class Post:
    def __init__(self, path, root_dir=''):
        self.urlpath = os.path.splitext(path)[0]
        self.filepath = os.path.join(root_dir, path)
        self.published = False
        self._initialize_metadata()

    @cached_property
    def html(self):
        with open(self.filepath, 'r') as fin:
            content = fin.read().split('\n\n', 1)[1].strip()
        return markdown.markdown(content, extensions=["codehilite(linenums=True)"])

    def url(self, _external=False):
        return url_for('post', path=self.urlpath, _external=_external)

    def _initialize_metadata(self):
        content = ''
        with open(self.filepath, 'r') as fin:
            for line in fin:
                if not line.strip():
                    break
                content += line
        self.__dict__.update(yaml.load(content))
        if hasattr(self, 'tags'):
            self.tags = [tag.strip() for tag in self.tags.split(',')]
        else:
            self.tags = []

app = Flask(__name__)

import settings
app.config.from_object(settings)
blog = Blog(app, 'posts')
freezer = Freezer(app)

@app.template_filter('date')
def format_date(value, format="%B %d, %Y"):
    return value.strftime(format)

#app.jinja_env.filters['date'] = format_date
#@app.context_processor
#def injext_format_date():
#    return {'format_date': format_date}

@app.route('/')
def index():
    return render_template('index.html', posts=blog.posts)

@app.route('/blog/<path:path>/')
def post(path):
#    path = path.strip('/')
    post = Post(path+settings.POSTS_FILE_EXTENSION, root_dir='posts')
    return render_template('post.html', post=post)

@app.route('/feed.atom')
def feed():
    feed = AtomFeed('Recent Posts',
            feed_url = request.url,
            url = request.url_root)
    posts = blog.posts[:10]
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


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'build':
        freezer.freeze()
    else:
        app.run(port=8000, debug=True)
