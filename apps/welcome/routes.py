from apps.welcome import blueprint
from flask import render_template, redirect, request, url_for,flash
from flask_login import current_user
from jinja2 import TemplateNotFound
import json 
from apps.forms import ContactForm
from apps.models import ContactUS
from datetime import datetime
@blueprint.route('/')
def route_default():
    '''try:
        if current_user.is_authenticated:
            return render_template(
                "home/home.html",
                user_name=current_user.name,
                user_email=current_user.email,
                user_profile_pic=current_user.profile_pic,
            )
        else:
            return render_template("welcome/index.html")
    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500'''
    return redirect(url_for('welcome_blueprint.welcome'))
@blueprint.route('/welcome',)
def welcome():
    contactUs=ContactForm()
    with open('apps/static/assets/data/data.json') as file:
        data=json.load(file)
    return render_template('welcome/index.html', segment='welcome',data=data,form=contactUs)

@blueprint.route('/submit-contact', methods=['GET', 'POST'])
def submit_contact():
    form = ContactForm(request.form)
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.msg.data

        # Save the data in MongoDB using mongoengine
        contact_us = ContactUS(name=name, email=email, message=message,created_at=datetime.now())
        contact_us.save()
        return render_template('welcome/thanks.html', segment='thank you!')
    else:
        return redirect(url_for('welcome_blueprint.welcome'))
@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500