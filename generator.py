import os
import markdown
import yaml
from flask import Flask, render_template, url_for, abort
from werkzeug import cached_property


POSTS_FILE_EXTENSION = '.md'

class Blog:
    def __init__(self, app, root_dir, file_ext = POSTS_FILE_EXTENSION):
        self._app = app
        self.root_dir = root_dir
        self.ext = file_ext
        self._cache = {}
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
        return self._cache.values()

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
        self._initialize_metadata()

    @cached_property
    def html(self):
        with open(self.filepath, 'r') as fin:
            content = fin.read().split('\n\n', 1)[1].strip()
        return markdown.markdown(content)

    @property
    def url(self):
        return url_for('post', path=self.urlpath)

    def _initialize_metadata(self):
        content = ''
        with open(self.filepath, 'r') as fin:
            for line in fin:
                if not line.strip():
                    break
                content += line
        self.__dict__.update(yaml.load(content))

app = Flask(__name__)
blog = Blog(app, 'posts')

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

@app.route('/blog/<path:path>')
def post(path):
    path = path.strip('/')
    post = Post(path+POSTS_FILE_EXTENSION, root_dir='posts')
    return render_template('post.html', post=post)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
