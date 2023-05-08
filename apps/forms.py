# -*- encoding: utf-8 -*-


from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SelectField, SelectMultipleField, IntegerField,SubmitField
from wtforms.validators import Email, DataRequired, Regexp, NumberRange,EqualTo

from flask_wtf.file import FileField, FileAllowed, FileRequired

# login and registration


class LoginForm(FlaskForm):
    email = TextField('Email',
                      id='email_create',
                      validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             id='pwd_login',
                             validators=[DataRequired()])


class CreateAccountForm(FlaskForm):
    username = TextField('Username',
                         id='username_create',
                         validators=[DataRequired()])
    email = TextField('Email',
                      id='email_create',
                      validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             id='pwd_create',
                             validators=[DataRequired()])
    password_confirm = PasswordField('Password',
                             id='pwd_create',
                             validators=[DataRequired(),EqualTo("password_confirm", message="Passwords Don't match!!!")])


class RunChecker(FlaskForm):
    
    model = FileField('Model', validators=[FileRequired()])
        #FileAllowed(['h5'], 'h5 files only!')''''''
    dataset = SelectField('Dataset',
                         id='dataset_run',
                         validators=[DataRequired()],
                         choices=[("mnist","MNIST"),
                                  ("fashion_mnist","Fashion MNIST"),
                                  ("cifar10","CIFAR10")])
    criteria = SelectField('criteria',
                            id='criteria_run',
                            validators=[DataRequired()],
                            choices=[('nc','Neuron Coverage'), 
                                      ('nc_BFS', 'Neuron Coverage with BFS heuristic'),
                                      ('ssc','Sign-Sign Coverage'),
                                      ('ssc_BFS','Sign-Sign Coverage with BFS heuristic '),
                                      ('nbc','Neuron Boudary Coverage')])
    norm = SelectField('Norm',
                         id='norm_run',
                         validators=[DataRequired()],
                         choices=[("l0","L0"),
                                  ("linf","Linfini")])
    submit = SubmitField(label="run")