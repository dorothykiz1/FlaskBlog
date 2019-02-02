from flask_wtf import FlaskForm
from wtforms import StringField ,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired ,Length,Email,EqualTo
# data required validator major fo not laving the field empty

# class RegistrationForm-child inherits from Flaskform parent class

class RegistrationForm(FlaskForm):
     """ 
        no making it empty n btn 2-20 
        characters -add
        validators
        
    """
    Username = StringField('username', validators=[DataRequired(), Length(min=2,max=20)]
    Email =StringField('email',validators=[DataRequired(),Email()])
    Password= PasswordField('password',validators=[DataRequired()])
    confirm_password= PasswordField('confirm_password',
                    validators=[DataRequired(),EqualTo('Password')])
    Submit =SubmitField('Signup')
    
class LoginForm(FlaskForm):
     # username =StringField('username',
    #                        validators=[DataRequired(), Length(min=2,max=20)])
    # no making it empty n btn 2-20 characters -add validators
    Email =StringField('email',validators=[DataRequired(),Email()])
    Password= PasswordField('password',validators=[DataRequired()])
    # Confirm_password= PasswordField('confirm_password',
    #                 validators=[DataRequired(),EqualTo('Password')])
    Remember =BooleanField('remember_me')
    Submit =SubmitField('Login')
    