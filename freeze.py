#!flask/bin/python
from app import app
from flask.ext.frozen import Freezer

freezer = Freezer(app)
freezer.freeze()
