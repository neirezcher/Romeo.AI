# -*- encoding: utf-8 -*-


from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SelectField, SelectMultipleField, IntegerField,SubmitField,TextAreaField
from wtforms.validators import Email, DataRequired, Regexp, NumberRange,EqualTo,Optional,Length

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

# deepconcolic params input
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
                                      ('ssc','Sign-Sign Coverage'),
                                      ('bfc','Neuron Boudary Coverage')])
    norm = SelectField('Norm',
                         id='norm_run',
                         validators=[DataRequired()],
                         choices=[("l0","L0"),
                                  ("linf","Linfini")])
    submit = SubmitField(label="Run")
class ContactForm(FlaskForm):
    name = TextField('Name',
                      id='name',
                      validators=[DataRequired()])
    email = TextField('Email',
                      id='email',
                      validators=[DataRequired(), Email()])
  
    msg=TextAreaField(u'Mailing Address',id='message',validators=[Optional(),Length(max=200)])