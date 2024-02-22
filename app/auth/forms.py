from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.auth.models import User

class MyBaseForm(FlaskForm):
    class Meta:
        locales = ['ru']
        def get_translations(self, form):
            return super(FlaskForm.Meta, self).get_translations(form)


class LoginForm(MyBaseForm):
    # Валидатор DataRequiredпросто проверяет, что поле не заполнено пустым
    username = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    # remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
    
class RegistrationForm(MyBaseForm):   
    username = StringField('Логин - убрать', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField(
        'Повтор пароля', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Регистрация')
    
    def validate_email(self, email):
        user = User().get(login=email.data)
        if user is not None:
            raise ValidationError('Пожалуйста введите другой email.')
        

class ResetPasswordRequestForm(MyBaseForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Сбросить пароль')

class ResetPasswordForm(MyBaseForm):
    password = PasswordField('Новый пароль', validators=[DataRequired()])
    password2 = PasswordField(
        'Повтор пароля', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Сбросить пароль')