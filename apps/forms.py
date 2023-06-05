# -*- encoding: utf-8 -*-


from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SelectField, SelectMultipleField, IntegerField,SubmitField,TextAreaField,StringField
from wtforms.validators import Email, DataRequired, Regexp, NumberRange,EqualTo,Optional,Length
from wtforms.widgets import HiddenInput
from flask_wtf.file import FileField, FileAllowed, FileRequired

# login and registration


class LoginForm(FlaskForm):
    email = TextField('Email',
                      id='email_create',
                      validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             id='pwd_login',
                             validators=[DataRequired()])

class ResetPasswordForm(FlaskForm):
    email = TextField('Email',
                      id='email_create',
                      validators=[DataRequired(), Email()])
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
    model = FileField('Model',validators=[FileRequired(),FileAllowed(['h5'], 'Only H5 files are allowed.')])
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
class UserProfileForm(FlaskForm):
    username = StringField('Username', render_kw={'readonly': True})
    email = StringField('Email', render_kw={'readonly': True})
    firstname = StringField('First Name', validators=[Optional()])
    lastname = StringField('Last Name', validators=[Optional()])
    city = StringField('City', validators=[Optional()])
    country = StringField('Country', validators=[Optional()])
    about_me = TextAreaField('About Me', validators=[Optional()])
    submit = SubmitField('Save Changes')

class ProfileImageForm(FlaskForm):
    profile_image = FileField('Profile Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Upload')
class SendEmailsForm(FlaskForm):
    question = StringField('Question', render_kw={'readonly': True})
    subject = StringField('Subject', validators=[DataRequired()])
    body = TextAreaField('Email Body', validators=[DataRequired()])
class AddUserForm(FlaskForm):
    username = TextField('Username',
                         id='username_create',
                         validators=[DataRequired()])
    email = TextField('Email',
                      id='email_create',
                      validators=[DataRequired(), Email()])
    firstname = StringField('First Name', validators=[Optional()])
    lastname = StringField('Last Name', validators=[Optional()])
    country = SelectField('country',
                            id='country',
                            validators=[Optional()],
                            choices=[('argentina','ARGENTINA'), 
                                      ('australia','AUSTRALIA'),
                                      ('austria','AUSTRIA'),
                                      ('bahrain','BAHRAIN'),
                                      ('bangladesh','BANGLADESH'),
                                      ('barbados','BARBADOS'),
                                      ('belarus','BELARUS'),
                                      ('belgium','BELGIUM'),
                                      ('belize','BELIZE'),
                                      ('benin','BENIN'),
                                      ('bhutan','BHUTAN'),
                                      ('bolivia','BOLIVIA'),
                                      ('botswana','BOTSWANA'),
                                      ('brazil','BRAZIL'),
                                      ('bulgaria','BULGARIA'),
                                      ('burkina faso','BURKINA FASO'),
                                      ('burundi','BURUNDI'),
                                      ('cambodia','CAMBODIA'),
                                      ('canada','CANADA'),
                                      ('cape verde','CAPE VERDE'),
                                      ('central african rep.','CENTRAL AFRICAN REP.'),
                                      ('chile','CHILE'),
                                      ('china','CHINA'),
                                      ('colombia','COLOMBIA'),
                                      ('costa rica','COSTA RICA'),
                                      ('croatia','CROATIA'),
                                      ('cyprus','CYPRUS'),
                                      ('czech','CZECH REPUBLIC'),
                                      ('denmark','DENMARK'),
                                      ('dominica','DOMINICA'),
                                      ('dominican republic','DOMINICAN REPUBLIC'),
                                      ('ecuador','ECUADOR'),
                                      ('egypt','EGYPT'),
                                      ('el salvador','EL SALVADOR'),
                                      ('aquatorial guinea','EQUATORIAL GUINEA'),
                                      ('estonia','ESTONIA'),
                                      ('ethiopia','ETHIOPIA'),
                                      ('fiji','FIJI'),
                                      ('finland','FINLAND'),
                                      ('france','FRANCE'),
                                      ('greece','GREECE'),
                                      ('guatemala','GUATEMALA'),
                                      ('guinea-bissau','GUINEA-BISSAU'),
                                      ('guyana','GUYANA'),
                                      ('honduras','HONDURAS'),
                                      ('hungary','HUNGARY'),
                                      ('iceland','ICELAND'),
                                      ('india','INDIA'),
                                      ('indinesia','INDONESIA'),
                                      ('iran','IRAN'),
                                      ('ireland','IRELAND'),
                                      ('israel','ISRAEL'),
                                      ('italy','ITALY'),
                                      ('jamaica','JAMAICA'),
                                      ('japan','JAPAN'),
                                      ('jordan','JORDAN'),
                                      ('kazakhstan','KAZAKHSTAN'),
                                      ('kenya','KENYA'),
                                      ('korea','KOREA'),
                                      ('kuwait','KUWAIT'),
                                      ('kyrgyz republic','KYRGYZ REPUBLIC'),
                                      ('latvia','LATVIA'),
                                      ('lithuania','LITHUANIA'),
                                      ('macebonia fyr','MACEDONIA, FYR'),
                                      ('madagascar','MADAGASCAR'),
                                      ('malawi','MALAWI'),
                                      ('malaysia','MALAYSIA'),
                                      ('malta','MALTA'),
                                      ('mauritius','MAURITIUS'),
                                      ('mexico','MEXICO'),
                                      ('mongolia','MONGOLIA'),
                                      ('morocco','MOROCCO'),
                                      ('mozambique','MOZAMBIQUE'),
                                      ('myanmar','MYANMAR'),
                                      ('nepal','NEPAL'),
                                      ('netherlands','NETHERLANDS'),
                                      ('new zealand','NEW ZEALAND'),
                                      ('nicaragua','NICARAGUA'),
                                      ('niger','NIGER'),
                                      ('nigeria','NIGERIA'),
                                      ('norway','NORWAY'),
                                      ('oman','OMAN'),
                                      ('pakistan','PAKISTAN'),
                                      ('panama','PANAMA'),
                                      ('papua new guinea','PAPUA NEW GUINEA'),
                                      ('paraguay','PARAGUAY'),
                                      ('peru','PERU'),
                                      ('philippines','PHILIPPINES'),
                                      ('poland','POLAND'),
                                      ('portugal','PORTUGAL'),
                                      ('qatar','QATAR'),
                                      ('romania','ROMANIA'),
                                      ('russia','RUSSIA'),
                                      ('rwanda','RWANDA'),
                                      ('saudi arabia','SAUDI ARABIA'),
                                      ('senegal','SENEGAL'),
                                      ('sierra leone','SIERRA LEONE'),
                                      ('singapore','SINGAPORE'),
                                      ('slovak republic','SLOVAK REPUBLIC'),
                                      ('slovenia','SLOVENIA'),
                                      ('south africa','SOUTH AFRICA'),
                                      ('spain','SPAIN'),
                                      ('sri lanka','SRI LANKA'),
                                      ('st. kitts anad nevis','ST. KITTS AND NEVIS'),
                                      ('st; lucia','ST. LUCIA'),
                                      ('st. vincent & grens','ST. VINCENT & GRENS.'),
                                      ('sweden','SWEDEN'),
                                      ('switzerland','SWITZERLAND'),
                                      ('tanzania','TANZANIA'),
                                      ('thailand','THAILAND'),
                                      ('trinidad','TRINIDAD AND TOBAGO '),
                                      ('tunisia','TUNISIA'),
                                      ('turkey','TURKEY'),
                                      ('uganda','UGANDA'),
                                      ('ukraine','UKRAINE'),
                                      ('united kingdom','UNITED KINGDOM'),
                                      ('uruguay','URUGUAY'),
                                      ('venezuela','VENEZUELA'),
                                      ('vietnam','VIETNAM'),
                                      ('yemen','YEMEN'),
                                      ('zimbabwe','ZIMBABWE')
                                      ],render_kw={'size': 5})
    city = StringField('city', validators=[Optional()])
    submit = SubmitField('Add user')
class ChangePasswordForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=6)
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        EqualTo('new_password', message='Passwords must match')
    ])