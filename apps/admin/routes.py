from apps.admin import blueprint
from flask import render_template, request,redirect,flash,url_for,jsonify,flash
from flask_login import login_required, current_user,logout_user
from jinja2 import TemplateNotFound
from apps.forms import SendEmailsForm,UserProfileForm,AddUserForm
from apps.models import User,ContactUS
from apps.admin.replyQuestions import sendMail
from apps.admin.sendPw import sendPassword
from apps.authentication.util import hash_pass
from apps import db, app
from werkzeug.utils import secure_filename
import os, stat
from bson import ObjectId,json_util
from decouple import config
import pandas as pd
import base64
from datetime import datetime
@blueprint.route('/all-Messages')
@login_required
def all_messages():
    if current_user.role == 'admin':
        # Retrieve all contact us messages sorted by creation date in descending order
        num_members = User.objects.count()
        num_reports = len(current_user.list_run)
        messages = ContactUS.objects.order_by('-created_at')
        num_messages = len(messages)
        if current_user.profile_image:
            # Read the data of the profile image
            image_data = current_user.profile_image.read()

            # Convert the image data to base64
            base64_image = base64.b64encode(image_data).decode('utf-8')

            # Generate the HTML <img> tag with the base64-encoded image data
            profile_image_url  = f"data:image/jpeg;base64,{base64_image}"
        else:
            profile_image_url = None
        return render_template("admin/allMessages.html", segment="select",messages=messages, num_messages=num_messages,current_datetime=datetime.now(),num_members=num_members,num_reports=num_reports,profile_image_url=profile_image_url)
    else:
        return render_template("home/page-403.html"), 403
@blueprint.route('/reply-Message/<message_id>',methods=['GET', 'POST'])
@login_required
def reply_message(message_id):
    if current_user.role == 'admin':
        num_members = User.objects.count()
        num_messages= ContactUS.objects.count()
        num_reports = len(current_user.list_run)
        if current_user.profile_image:
            # Read the data of the profile image
            image_data = current_user.profile_image.read()

            # Convert the image data to base64
            base64_image = base64.b64encode(image_data).decode('utf-8')

            # Generate the HTML <img> tag with the base64-encoded image data
            profile_image_url  = f"data:image/jpeg;base64,{base64_image}"
        else:
            profile_image_url = None
        messages = ContactUS.objects(replied=False).order_by('-created_at').limit(5)
        '''------------------------------------------------------------------'''
        message = ContactUS.objects.get(id=message_id)
        form = SendEmailsForm()
        print(form.validate_on_submit())
        try:
            if form.validate_on_submit():
                # Retrieve the current user from the database
                subject = form.subject.data
                body = form.body.data
                sendMail(message.email,message.name,subject, body)
                message.replied = True
                # Save the changes to the database
                message.save()
                flash('Profile updated successfully.', 'success')
                return redirect(url_for('admin_blueprint.all_messages'))
        except:
                flash('Something went wrong.', 'error')
        # Populate the form fields with the current user's data
        form.question.data = message.message

        return render_template("admin/replyMessage.html", segment="select",message=message, num_messages=num_messages,num_members=num_members,num_reports=num_reports,profile_image_url=profile_image_url,form=form,messages=messages)
    else:
        return render_template("home/page-403.html"), 403
@blueprint.route('/users')
@login_required
def users():
    if current_user.role == 'admin':
        if current_user.profile_image:
            # Read the data of the profile image
            image_data = current_user.profile_image.read()

            # Convert the image data to base64
            base64_image = base64.b64encode(image_data).decode('utf-8')

            # Generate the HTML <img> tag with the base64-encoded image data
            profile_image_url  = f"data:image/jpeg;base64,{base64_image}"
        else:
            profile_image_url = None
        users = User.objects.all()

        return render_template("admin/listUsers.html", users=users,profile_image_url=profile_image_url, segment='users')
    else:
        return render_template("home/page-403.html"), 403
@blueprint.route('/delete_user/<user_id>', methods=['GET'])
@login_required
def delete_user(user_id):
    if current_user.role == 'admin':
        # Retrieve the user with the provided ID
        user = User.objects.get(id=user_id)
        
        # Delete the user
        user.delete()
        
        # Redirect to a success page or another route
        return redirect(url_for('admin_blueprint.users'))
    else:
        return render_template("home/page-403.html"), 403
@blueprint.route('/edit-profile/<user_id>', methods=['GET', 'POST'])
@login_required
def edit_profile(user_id):
    if current_user.role == 'admin':
        form = UserProfileForm()
        # Retrieve the current user from the database
        user = User.objects.get(id=ObjectId(user_id))
        print(form.validate_on_submit())
        if form.validate_on_submit():
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
            return redirect(url_for('admin_blueprint.edit_profile',user_id=user_id))

        # Populate the form fields with the current user's data
        form.username.data = user.username
        form.email.data = user.email
        form.firstname.data = user.firstname
        form.lastname.data = user.lastname
        form.city.data = user.city
        form.country.data = user.country
        form.about_me.data = user.about_me
        if user.profile_image:
            # Read the data of the profile image
            image_data = user.profile_image.read()

            # Convert the image data to base64
            base64_image = base64.b64encode(image_data).decode('utf-8')

            # Generate the HTML <img> tag with the base64-encoded image data
            user_image_url  = f"data:image/jpeg;base64,{base64_image}"
        else:
            user_image_url = None
        if current_user.profile_image:
            # Read the data of the profile image
            image_data = current_user.profile_image.read()

            # Convert the image data to base64
            base64_image = base64.b64encode(image_data).decode('utf-8')

            # Generate the HTML <img> tag with the base64-encoded image data
            profile_image_url  = f"data:image/jpeg;base64,{base64_image}"
        else:
            profile_image_url = None
        return render_template('admin/editUser.html',segment='list', form=form,profile_image_url=profile_image_url,user_image_url=user_image_url,user=user)
    else:
        return render_template("home/page-403.html"), 403



@blueprint.route('/admin/upload_image/<user_id>', methods=['POST'])
@login_required
def upload_image(user_id):
    if current_user.role == 'admin':
        image = request.files['image']
        user = User.objects.get(id=ObjectId(user_id))
        if user.profile_image:  # Check if a profile image already exists
            user.profile_image.replace(image, content_type=image.content_type)
        else:
            user.profile_image.put(image, content_type=image.content_type)
        user.save()
        return redirect(url_for('admin_blueprint.edit_profile',user_id=user_id))
    else:
        return render_template("home/page-403.html"), 403

@blueprint.route('/add-user', methods=['GET', 'POST'])
@login_required
def addUser():
    if current_user.role == 'admin':
        if current_user.profile_image:
            # Read the data of the profile image
            image_data = current_user.profile_image.read()

            # Convert the image data to base64
            base64_image = base64.b64encode(image_data).decode('utf-8')

            # Generate the HTML <img> tag with the base64-encoded image data
            profile_image_url  = f"data:image/jpeg;base64,{base64_image}"
        else:
            profile_image_url = None
        form = AddUserForm()

        if form.validate_on_submit():
            firstname, lastname, city, country= None,None,None,None
            username = form.username.data
            email = form.email.data
            #Generate Random Pass and Set it to User object		
            import random		
            s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"		
            passlen = 16		
            generated_password = "".join(random.sample(s,passlen ))
            if form.firstname.data:
                firstname = form.firstname.data
            if form.lastname.data:
                lastname = form.lastname.data
            if form.city.data:
                city = form.city.data
            if form.country.data:
                country = form.country.data
            user = User(email=email,
                        username=username,
                        password=hash_pass(generated_password),
                        firstname=firstname,
                        lastname=lastname,
                        city=city,
                        country=country)
            user.save()
            sendPassword(email,generated_password)
            return redirect(url_for('admin_blueprint.users'))

        return render_template('admin/addUser.html', form=form, profile_image_url=profile_image_url,segment='addUser')
    else:
        return render_template("home/page-403.html"), 403