from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.auth.models import User

class MyBaseForm(FlaskForm):
    class Meta:
        locales = ['ru']
        def get_translations(self, form):
            return super(FlaskForm.Meta, self).get_translations(form)


    # def validate_username(self, username):
    #     user = User().get(login=username.data)
    #     if user is not None:
    #         raise ValidationError('Please use a different username.')

        
class EditProfileForm(MyBaseForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')
    
class EmptyForm(MyBaseForm):
    submit = SubmitField('Submit')