# -*- encoding: utf-8 -*-
from apps.home import blueprint
from flask import render_template, request,redirect,flash,url_for,jsonify,flash,send_file
from flask_login import login_required, current_user,logout_user
from jinja2 import TemplateNotFound
from apps.forms import RunChecker,UserProfileForm,ChangePasswordForm
from apps.models import User,Deepconcorun,ReportChunk
from apps.authentication.util import hash_pass
import subprocess
import docker
from apps import db, app
from werkzeug.utils import secure_filename
import os, stat, io
from bson import ObjectId,json_util
import json
from decouple import config
import pandas as pd
import base64

@blueprint.route('/home')
@login_required
def home():
    if current_user.is_authenticated:
        if current_user.profile_image:
            # Read the data of the profile image
            image_data = current_user.profile_image.read()

            # Convert the image data to base64
            base64_image = base64.b64encode(image_data).decode('utf-8')

            # Generate the HTML <img> tag with the base64-encoded image data
            profile_image_url  = f"data:image/jpeg;base64,{base64_image}"
        else:
            profile_image_url = None
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
            heatmap_data = []
            for key, array in last_record.heatmap_matrix.items():
                for i, value in enumerate(array):
                    heatmap_data.append({'group': key, 'variable': i, 'value': value})
            print(heatmap_data)
            # Convert the data to a DataFrame
            df = pd.DataFrame(heatmap_data)
            # Export the DataFrame to a CSV file
            csv_file_relative_path = 'apps/static/assets/csv/heatmap_data.csv'
            df.to_csv( csv_file_relative_path, encoding='utf-8', index=False)
            # Get the absolute file path
            csv_file_path = os.path.abspath(csv_file_relative_path)

            # Get the current file permissions
            current_permissions = os.stat(csv_file_path).st_mode

            # Add read permission for the web server
            new_permissions = current_permissions | stat.S_IRGRP | stat.S_IROTH

            # Set the new permissions on the file
            os.chmod(csv_file_path, new_permissions)
            # Pass the data to the template
            return render_template('home/home.html',segment='home', last_record=last_record, last_records=last_records_list, json_data=json_data,profile_image_url=profile_image_url)

    # Pass the data to the template
    #return render_template('home/home.html', segment='home', data=data_list)
    return redirect(url_for('home_blueprint.check_Model'))
    


@blueprint.route('/<template>')
@login_required
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
@blueprint.route("/json-users")
def users():
    return jsonify(User.objects)

@blueprint.route('/check_Model', methods=['GET','POST'])
@login_required
def check_Model():
    if current_user.profile_image:
        # Read the data of the profile image
        image_data = current_user.profile_image.read()

        # Convert the image data to base64
        base64_image = base64.b64encode(image_data).decode('utf-8')

        # Generate the HTML <img> tag with the base64-encoded image data
        profile_image_url  = f"data:image/jpeg;base64,{base64_image}"
    else:
        profile_image_url = None
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
    return render_template('home/form.html', form=Deepconcolic_form, segment='form',profile_image_url=profile_image_url)
@blueprint.route('/report/<report_id>')
@login_required
def get_report(report_id):
    if current_user.profile_image:
        # Read the data of the profile image
        image_data = current_user.profile_image.read()

        # Convert the image data to base64
        base64_image = base64.b64encode(image_data).decode('utf-8')

        # Generate the HTML <img> tag with the base64-encoded image data
        profile_image_url  = f"data:image/jpeg;base64,{base64_image}"
    else:
        profile_image_url = None
    deepconcorun = Deepconcorun.objects.get(_id=report_id)
    json_data = json.dumps(deepconcorun.class_robustness)
    heatmap_data = []
    for key, array in deepconcorun.heatmap_matrix.items():
        for i, value in enumerate(array):
            heatmap_data.append({'group': key, 'variable': i, 'value': value})
    #print(heatmap_data)
    # Convert the data to a DataFrame
    df = pd.DataFrame(heatmap_data)
    # Export the DataFrame to a CSV file
    csv_file_relative_path = 'apps/static/assets/csv/heatmap_data.csv'
    df.to_csv( csv_file_relative_path, encoding='utf-8', index=False)
    # Get the absolute file path
    csv_file_path = os.path.abspath(csv_file_relative_path)

    # Get the current file permissions
    current_permissions = os.stat(csv_file_path).st_mode

    # Add read permission for the web server
    new_permissions = current_permissions | stat.S_IRGRP | stat.S_IROTH

    # Set the new permissions on the file
    os.chmod(csv_file_path, new_permissions)

    return render_template('home/report.html',segment='view', deepconcorun=deepconcorun, json_data=json_data,profile_image_url=profile_image_url)

@blueprint.route('/list-report')
@login_required
def list_report():
    if current_user.profile_image:
        # Read the data of the profile image
        image_data = current_user.profile_image.read()

        # Convert the image data to base64
        base64_image = base64.b64encode(image_data).decode('utf-8')

        # Generate the base64-encoded image data
        profile_image_url  = f"data:image/jpeg;base64,{base64_image}"
    else:
        profile_image_url = None
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
            return render_template('home/List.html',segment='list', list=list_report,profile_image_url=profile_image_url)

    return render_template('home/EmptyList.html', segment='empty',profile_image_url=profile_image_url)

@blueprint.route('/delete-object', methods=['POST'])
@login_required
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
    
@blueprint.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = UserProfileForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        # Retrieve the current user from the database
        user = User.objects.get(id=current_user.id)

        # Update the user profile with the modified fields
        if form.firstname.data:
            user.firstname = form.firstname.data
        if form.lastname.data:
            user.lastname = form.lastname.data
        if form.city.data:
            user.city = form.city.data
        if form.country.data:
            user.country = form.country.data
        if form.about_me.data:
            user.about_me = form.about_me.data

        # Save the changes to the database
        user.save()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('home_blueprint.edit_profile'))

    # Populate the form fields with the current user's data
    form.username.data = current_user.username
    form.email.data = current_user.email
    form.firstname.data = current_user.firstname
    form.lastname.data = current_user.lastname
    form.city.data = current_user.city
    form.country.data = current_user.country
    form.about_me.data = current_user.about_me
    if current_user.profile_image:
        # Read the data of the profile image
        image_data = current_user.profile_image.read()

        # Convert the image data to base64
        base64_image = base64.b64encode(image_data).decode('utf-8')

        # Generate the HTML <img> tag with the base64-encoded image data
        profile_image_url  = f"data:image/jpeg;base64,{base64_image}"
    else:
        profile_image_url = None
    return render_template('home/profile.html',segment='list', form=form,profile_image_url=profile_image_url)




@blueprint.route('/delete-profile/<user_id>', methods=['GET'])
@login_required
def delete_profile(user_id):
    if current_user.is_authenticated and str(current_user.id) == user_id:
        User.objects(id=user_id).delete()
        # Log out the current user
        logout_user()
    return redirect(url_for('authentication_blueprint.login'))


@blueprint.route('/upload_image', methods=['POST'])
@login_required
def upload_image():
    image = request.files['image']
    if current_user.profile_image:  # Check if a profile image already exists
        current_user.profile_image.replace(image, content_type=image.content_type)
    else:
        current_user.profile_image.put(image, content_type=image.content_type)
    current_user.save()
    return redirect(url_for('home_blueprint.edit_profile'))

@blueprint.route('/download-report/<report_id>', methods=['GET'])
@login_required
def download_report(report_id):
    # Retrieve the Deepconcorun document with the desired reportref
    deepconcorun = Deepconcorun.objects.get(_id=report_id)  # Example: Get the first document
    # Retrieve the associated ReportMetadata document
    report_metadata = deepconcorun.reportref

    # Get the ObjectId of the associated report
    report_id = report_metadata._id

    # Retrieve the ReportChunk documents based on the files_id
    report_chunks = ReportChunk.objects(files_id=report_metadata._id).all()


    # Combine the data from the chunks to create a DataFrame
    data = b''
    for chunk in report_chunks:
        if isinstance(chunk.data, str):  # Check if the chunk data is a string
            chunk_data = chunk.data.encode('utf-8')  # Encode the string to bytes
        else:
            chunk_data = chunk.data
        data += chunk_data

    # Create a file-like object from the data
    data_file = io.BytesIO(data)

    # Load the data into a pandas DataFrame
    df = pd.read_excel(data_file, engine='openpyxl')  # Specify the correct encoding if needed

    # Create an Excel file from the DataFrame
    excel_file = io.BytesIO()
    with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)

    # Seek to the beginning of the Excel file
    excel_file.seek(0)

    return send_file(
        excel_file,
        as_attachment=True,
        download_name=report_metadata.filename,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    
    )  
    #if report_chunk:
        # Get the file data
        #file_data = report_chunk.data

        # Create a file-like object from the binary data
        #file_stream = io.BytesIO(file_data)

        # Read the data into a pandas DataFrame with the appropriate encoding
        #df = pd.read_excel(file_stream, engine='openpyxl')

        # Convert DataFrame to Excel format (XLSX)
        #excel_file_stream = io.BytesIO()
        #df.to_excel(excel_file_stream, index=False)
        #excel_file_stream.seek(0)

        # Send the Excel file as a download attachment
        #return send_file(excel_file_stream, download_name=report_metadata.filename + '.xlsx', as_attachment=True)
    # Return an appropriate response if the report_chunk is not found
    #return 'File not found', 404 '''
@blueprint.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_pwd():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        new_password = form.new_password.data
        hashed_password = hash_pass(new_password)

        # Update the password for the current user		
        
        current_user.password = hashed_password
        current_user.save()

        return redirect(url_for('home_blueprint.edit_profile'))  # Redirect to the profile page

    return render_template('home/changePassword.html', form=form)
    



