from flask_wtf import FlaskForm
from wtforms import StringField ,PasswordField,SubmitField,BooleanField,ValidationError
from wtforms.validators import DataRequired ,Length,Email,EqualTo
from Flaskblog.models import User
# data required validator major fo not laving the field empty

# class RegistrationForm-child inherits from Flaskform parent class

class RegistrationForm(FlaskForm):
    
    Username = StringField('username',validators= [DataRequired(), Length(min=2, max=20)])
    Email = StringField('email',validators= [DataRequired(), Email()])
    Password= PasswordField('password',validators= [DataRequired()])
    confirm_password= PasswordField('confirm_password', validators= [DataRequired(), EqualTo('Password')])
    Submit = SubmitField('Signup')
#function for validating whether or not the username is already there
    def validate_username(self,username):
        user = User.query.filter_by(username = Username.data).first()#first value
        if user:
            raise ValidationError('Username taken please choose another one')
    
    def validate_email(self,email):
        user = User.query.filter_by(email = Email.data).first()#first value
        if user:
            raise ValidationError('Email taken please choose another one')
    

class LoginForm(FlaskForm):
        # username =StringField('username',
    #                        validators=[DataRequired(), Length(min=2,max=20)])
    # no making it empty n btn 2-20 characters -add validators
    Email = StringField('email', validators = [DataRequired(), Email()])
    Password = PasswordField('password', validators = [DataRequired()])
    Remember = BooleanField('remember_me')
    Submit = SubmitField('Login')
    