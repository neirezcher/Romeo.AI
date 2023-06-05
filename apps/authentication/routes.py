# -*- encoding: utf-8 -*-


from flask import render_template, redirect, request, url_for,flash
from flask_login import (
    current_user,
    login_user,
    logout_user
)
from flask_dance.contrib.google import google
from flask_dance.contrib.github import github
from apps import db, login_manager
from apps.authentication import blueprint
from apps.forms import LoginForm, CreateAccountForm,ResetPasswordForm
from apps.models import User
from apps.authentication.util import verify_pass,hash_pass
from apps.admin.sendPw import sendPassword
from bson import ObjectId



'''
@blueprint.route('/')
def route_default():
    if current_user.is_authenticated:
        return render_template(
            "home.html",
            user_name=current_user.name,
            user_email=current_user.email,
            user_profile_pic=current_user.profile_pic,
        )
    else:
        return render_template("index.html")
    return redirect(url_for('authentication_blueprint.login'))


# Login & Registration
@login_manager.user_loader
def load_user(user_id):
     return User.objects(id=ObjectId(user_id)).first()'''

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        email = request.form['email']
        password = request.form['password']

        # Locate user
        user = User.objects(email= email).first()

        # Check the password
        if user and verify_pass(password, user.password):

            login_user(user, remember=True)
            return redirect(url_for('authentication_blueprint.login'))

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)
    return redirect(url_for('home_blueprint.home'))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']

        # Check usename exists
        user = User.objects(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = User.objects(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        user = User(email=request.form['email'],
                    username=request.form['username'],
                    password=hash_pass(request.form['password']))
        user.save()
        login_user(user)
        return redirect(url_for('home_blueprint.home'))

    else:
        return render_template('accounts/register.html', form=create_account_form)


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))
@blueprint.route("/forgot-password", methods=['GET', 'POST']) 
def forgot_password():	
    form = ResetPasswordForm(request.form)
    if request.method=='GET': 
        #Send the forgot password form		
        return render_template('accounts/resetPassword.html',form=form)	
    elif request.method=='POST' and form.validate_on_submit(): 		
        #Get the post data		
        email = form.email.data
        #Checks		
        errors = []		
        if email is None or email=='':			
            errors.append('Username is required')
            return flash('Username is required',category='danger'), render_template('accounts/resetPassword.html',form)	
        user = User.objects.get_or_404(email=email)	
        if user :			
            #Generate Random Pass and Set it to User object		
            import random		
            s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"		
            passlen = 16		
            generated_password = "".join(random.sample(s,passlen ))
            print(generated_password)		
            pw_hash = hash_pass(generated_password)
            user.password = pw_hash		
            user.save()	
            sendPassword(email,generated_password)		
            return redirect(url_for('authentication_blueprint.login'))
        else:
            errors.append('Username is required')
            return flash('user not found',category='danger'), render_template('accounts/resetPassword.html',form)	
@blueprint.route("/login/google")
def google_login():
		#Let flask-dance do its magic
		if not google.authorized:
			return redirect(url_for("google.login"))
		resp = google.get("/plus/v1/people/me")
		assert resp.ok, resp.text    
		#Get/Create user
		username = resp.json()['emails'][0]['value']
		try:
			user = User.objects.get(username=username)
		except:
			password = "UNUSABLE_PASSWORD"
			user = User(username=username, email=username, password=password)
			user.has_usable_password = False
			user.save()
		#Login the user
		login_user(user)
		return redirect(url_for('home_blueprint.home'))

@blueprint.route("/login/github")
def github_login():
    if not github.authorized:
        return redirect(url_for("github.login"))
    resp = github.get("/user")
    assert resp.ok
    username = resp.json()['emails'][0]['value']
    try:
        user = User.objects.get(username=username)
    except:
        password = "UNUSABLE_PASSWORD"
        user = User(username=username, email=username, password=password)
        user.has_usable_password = False
        user.save()
	#Login the user
    login_user(user)
    return redirect(url_for('home_blueprint.home'))
    #return "You are @{login} on GitHub".format(login=resp.json()["login"])

# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
