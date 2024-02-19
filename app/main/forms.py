from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length


class MyBaseForm(FlaskForm):
    class Meta:
        locales = ['ru']
        def get_translations(self, form):
            return super(FlaskForm.Meta, self).get_translations(form)

    
class EmptyForm(MyBaseForm):
    submit = SubmitField('Submit')
    
class SignForm(MyBaseForm):
    username = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Подписаться')