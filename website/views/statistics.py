from flask import Blueprint, render_template, request, flash, redirect, url_for

statistics = Blueprint('statistics', __name__,
                 template_folder='../templates/statistics',
                 url_prefix='/statistics/')

@statistics.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
