from flask_wtf import FlaskForm
from app.models import User
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import (DataRequired, 
                                Email, 
                                EqualTo, 
                                Length,
                                ValidationError)


# Registration form class definition
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # Method to validate username uniqueness
    def validate_username(self, username_to_validate):
        check_user = User.query.filter_by(username=username_to_validate.data).first()
        if check_user:
            raise ValidationError(f'{check_user.username} Already Exist')

    # Method to validate email uniqueness
    def validate_email(self, email_to_validate):
        check_email = User.query.filter_by(email=email_to_validate.data).first()
        if check_email:
            raise ValidationError(f'{check_email.email} Already exist')
        
# Login form class definition        
class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember_me = BooleanField(label='Remember Me')
    submit = SubmitField(label='Login')