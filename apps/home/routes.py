# -*- encoding: utf-8 -*-
from apps.home import blueprint
from flask import render_template, request,redirect,flash,url_for,jsonify
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from apps.forms import RunChecker
from apps.models import User
import subprocess
import docker
from apps import db, app
from werkzeug.utils import secure_filename
import os
@blueprint.route('/home')
#@login_required
def home():

    return render_template('home/home.html', segment='home')


@blueprint.route('/<template>')
#@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return 
    
#delete profile
@blueprint.route("/delete_account")
@login_required
def delete_account():
    current_user.delete()
    flash("account deleted!",category='success')
    return redirect(url_for('authentication_blueprint.login'))
@blueprint.route("/users")
def users():
    return jsonify(User.objects)

@blueprint.route('/check_Model', methods=['GET','POST'])
#@login_required
def check_Model():
    try:
        Deepconcolic_form = RunChecker()
        print(Deepconcolic_form.validate_on_submit())
        if Deepconcolic_form.is_submitted():
            print(Deepconcolic_form.model.data)
        if request.method == "POST" and Deepconcolic_form.validate_on_submit():
            modelname = secure_filename(Deepconcolic_form.model.data.filename)
            print(app.instance_path)
            Deepconcolic_form.model.data.save(os.path.join(
            app.root_path, 'uploads', modelname
             ) )
            dataset= Deepconcolic_form.dataset.data
            criteria= Deepconcolic_form.criteria.data
            norm= Deepconcolic_form.norm.data
            return redirect(url_for('home_blueprint.home'))
                #command='python3 -m Deepconcolic.deepconcolic.main --outputs outs/ --dataset {0} --model {1} --criterion {2} --norm {3} --save-all-tests --max-iterations {4}'.format(str(dataset),model,criteria,norm,num_iteration)
                #run=subprocess.run(command,shell=True, capture_output=True,text=True)
        else:
            flash(Deepconcolic_form.errors)
    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except Exception as e:
        print(e)
        return render_template('home/page-500.html'), 500
    return render_template('home/form.html', form=Deepconcolic_form, segment='form')
@blueprint.route('/get_results')
def get_results():
    pass


