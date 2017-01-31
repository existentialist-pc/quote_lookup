from . import main
from flask import render_template
from .funcs import top_lookup


@main.route('/')
def index():
    lookups = top_lookup(5)
    return render_template('index.html', lookups=lookups)