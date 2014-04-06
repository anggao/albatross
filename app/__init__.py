from flask import Flask

app = Flask(__name__)

import settings
app.config.from_object(settings)

# load yaml config file, customize the blog
import yaml
config = yaml.load(file('app/config.yaml', 'r'))

from app import views


