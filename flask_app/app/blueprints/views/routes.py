from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('menu.html')

@views.route('/itersolvers')
def itersolver():
    return render_template('itersolver.html')

@views.route('/image_compression')
def image_compression():
    return render_template('image_compression.html')

@views.route('/results')
def results():
    return render_template('results.html')
