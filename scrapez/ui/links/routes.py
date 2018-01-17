from flask import render_template
from . import links

@links.route('/')
def index():
    return render_template('links.html')
