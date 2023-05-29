# -*- encoding: utf-8 -*-
from apps.home import blueprint
from flask import render_template, request,redirect,flash,url_for,jsonify
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from apps.forms import RunChecker
from apps.models import User,Deepconcorun
import subprocess
import docker
from apps import db, app
from werkzeug.utils import secure_filename
import os
from bson import ObjectId,json_util
import json
from decouple import config
@blueprint.route('/home')
#@login_required
def home():
    if current_user.is_authenticated:
        user = User.objects(username=current_user.username).first()

        # Check if the list_run field contains elements
        if user.list_run:
            # Retrieve the last 10 records from list_run
            last_records = user.list_run[-10:]
            print(last_records)
            last_records_list = []
            for run_id in last_records:
                if isinstance(run_id, str):
                    run_id = ObjectId(run_id)
                run = Deepconcorun.objects(_id=run_id.id).first()
                last_records_list.append(run)

            # Retrieve the data for the last record
            last_record = last_records_list[-1] if last_records_list else None
            if last_record.state == 'On process':
                if len(last_records_list)>1:
                    last_record = last_records_list[-2]
                else:
                    return redirect(url_for('home_blueprint.list_report'))
            #json_data = json.dumps(last_record.class_robustness)
            json_data = json.dumps(last_record.class_robustness)
            print(json_data)
            # Pass the data to the template
            return render_template('home/home.html',segment='home', last_record=last_record, last_records=last_records_list, json_data=json_data)

    # Pass the data to the template
    #return render_template('home/home.html', segment='home', data=data_list)
    return redirect(url_for('home_blueprint.check_Model'))
    


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
            modelpath=os.path.join(app.root_path, 'uploads', modelname)
            Deepconcolic_form.model.data.save(modelpath)
            dataset= Deepconcolic_form.dataset.data
            criteria= Deepconcolic_form.criteria.data
            norm= Deepconcolic_form.norm.data
            new_deepconcorun=Deepconcorun(general_robustness=0,ssc_robustness=None,nc_robustness=None,nbc_robustness=None,class_robustness=None,heatmap_matrix=None,norm = norm,criteria=criteria,dataset =dataset,modelref = None,reportref=None,state='On process') 
            new_deepconcorun.save()
            current_user.list_run.append(new_deepconcorun._id)
            current_user.save()
            image_name=config('DOCKER_IMAGE')
            mountingPath=modelpath+':/app/saved_Models/'+modelname
            containerModelPath='saved_Models/'+modelname
            password = config('SHELL_PASSWORD')
            # Pull the Docker image with sudo and automatic password
            pull_command = f'echo {password} | sudo -S docker pull {image_name}'
            subprocess.call(pull_command, shell=True)
            # Run the Docker container with sudo and automatic password
            run_command = f'echo {password} | sudo -S docker run -v {mountingPath} -p 8080:8080 {image_name} --dataset {dataset} --model {containerModelPath} --criterion {criteria} --norm {norm} --user-email {current_user.email} --run-id {new_deepconcorun._id}'
            subprocess.call(run_command, shell=True)
            #subprocess.call(["sudo","docker", "pull", image_name]) 
            #subprocess.call(["sudo",'docker', 'run', '-v', mountingPath , '-p', '8080:8080', image_name , '--dataset', dataset , '--model', containerModelPath , '--criterion', criteria, '--norm', norm, '--user-email', current_user.email ,'--run-id',str(new_deepconcorun._id)])
            return redirect(url_for('home_blueprint.list_report'))
               
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
@blueprint.route('/list-report')
#@login_required
def list_report():
    if current_user.is_authenticated:
        user = User.objects(username=current_user.username).first()

        # Check if the list_run field contains elements
        if user.list_run:
            # Retrieve the last 10 records from list_run
            list_report = []
            for run_id in user.list_run:
                if isinstance(run_id, str):
                    run_id = ObjectId(run_id)
                run = Deepconcorun.objects(_id=run_id.id).first()
                list_report.append(run)
            # Pass the data to the template
            return render_template('home/List.html',segment='list', list=list_report)
    return render_template('home/EmptyList.html', segment='empty')

@blueprint.route('/delete-object', methods=['POST'])
def delete_object():
    try:
        object_id = request.form.get('object_id')
        object = Deepconcorun.objects(_id=object_id).first()

        if object:
            user = User.objects(username=current_user.username).first()

            if user:
                
                
                user.list_run.remove(object)
                user.save()

            
            else:
                return jsonify({'success': False, 'message': 'User not found'}), 404

            object.delete()

        
        return redirect(url_for('home_blueprint.list_report'))


    except Deepconcorun.DoesNotExist:
        return jsonify({'success': False, 'message': 'Object not found'}), 404

    except Exception as e:
        print(e)
        return jsonify({'success': False, 'message': str(e)}), 400

 