from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField ,PasswordField,SubmitField,BooleanField,ValidationError
from wtforms.validators import DataRequired ,Length,Email,EqualTo
from Flaskblog.models import User
# data required validator major fo not laving the field empty

# class RegistrationForm-child inherits from Flaskform parent class

class RegistrationForm(FlaskForm):
    
    username = StringField('Username',validators= [DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators= [DataRequired(), Email()])
    password= PasswordField('Password',validators= [DataRequired()])
    confirm_password= PasswordField('Confirm_password', validators= [DataRequired(), EqualTo('Password')])
    submit = SubmitField('Signup')
#function for validating whether or not the username is already there
    def validate_username(self,username):
        user = User.query.filter_by(username = username.data).first()#first value
        if user:
            raise ValidationError('Username taken please choose another one')
    
    def validate_email(self,email):
        user = User.query.filter_by(email = email.data).first()#first value
        if user:
            raise ValidationError('Email taken please choose another one')
            
class LoginForm(FlaskForm):

     #making it empty n btn 2-20 characters -add validators
    email = StringField('Email', validators = [DataRequired(), Email()])
    password= PasswordField('Password',validators= [DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
     
    username = StringField('Username',validators= [DataRequired(), 
                            Length(min=2, max=20)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    email = StringField('Email',validators= [DataRequired(), Email()])
    submit = SubmitField('Update')
    #function for validating whether or not the username is already there
    def validate_username(self,username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()#first value
            if user:
                raise ValidationError('Username taken please choose another one')
        
    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()#first value
            if user:
                raise ValidationError('Email taken please choose another one')
        
    