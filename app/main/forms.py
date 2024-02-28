from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from wtforms.widgets import TextArea

class MyBaseForm(FlaskForm):
    class Meta:
        locales = ['ru']
        def get_translations(self, form):
            return super(FlaskForm.Meta, self).get_translations(form)

    
class EmptyForm(MyBaseForm):
    submit = SubmitField('Submit')
    
class SubscribeForm(MyBaseForm):
    email = StringField(label='@',validators=[DataRequired(), Email()], render_kw={"placeholder": "Введите email"})
    submit = SubmitField('Подписаться')
    
class TestForm(MyBaseForm):
    email = StringField(label='@',validators=[DataRequired(), Email()], render_kw={"placeholder": "Введите email"})
    submit = SubmitField('Подписаться')
    
class ContactForm(MyBaseForm):
    name = StringField(label='Ваше имя',validators=[DataRequired()], render_kw={"placeholder": "Введите Ваше имя"})
    email = StringField(label='Email',validators=[DataRequired(), Email()], render_kw={"placeholder": "Введите email для ответа"})
    message = StringField(label='Сообщение', widget=TextArea(), validators=[DataRequired()], render_kw={"placeholder": "Напишите Ваш вопрос и номер заказа. Мы обязательно ответим. Спасибо."}) 
    # submit = SubmitField('<i class="far fa-envelope"></i> Отправить')
    submit = SubmitField('Отправить')