from flask import Blueprint, render_template
from flask_login import login_required

site = Blueprint('site', __name__, template_folder='site_templates')

"""
Note that in the above code,
some arguments are specified when creating a blueprint objectc.
The first argument, 'site', is the Blueprint name as a string,
which is used by flask's routing machnism.
The second argument __name__ is the Blueprint's import name,
which Flask uses to locate the Blueprint's resources.
The third is telling Flask where to find the html to render. 
"""


@site.route('/')
def home():
    return render_template('index.html')
    

@site.route('/profile')
@login_required
def profile():
    return render_template('profile.html')
