from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from wtforms.widgets import TextArea
from markupsafe import Markup

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
        
class ContactForm(MyBaseForm):
    name = StringField(label='Ваше имя', validators=[DataRequired()], render_kw={"placeholder": "Введите Ваше имя"})
    email = StringField(label='Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Введите email для ответа"})
    message = StringField(label='Сообщение', widget=TextArea(), validators=[DataRequired()], render_kw={"placeholder": "Напишите Ваш вопрос и номер заказа. Мы обязательно ответим. Спасибо."}) 
    submit = SubmitField('Отправить')
    
class FreeForm(MyBaseForm):
    url = StringField(label='Ссылка на объявления', validators=[DataRequired()], render_kw={"placeholder": ""}) 
    email = StringField(label='Ваш Email',validators=[DataRequired(), Email()])
    checkPD = BooleanField("Я даю соглаcие на обработку персональных данных", validators=[DataRequired()], default=True, render_kw ={'checked':''})
    submit = SubmitField("Скачать данные")
        
class CalcForm(MyBaseForm):
    url = StringField(label='Ссылки с доски объявлений (одна или несколько)', widget=TextArea(), validators=[DataRequired()], render_kw={"placeholder": ""}) 
    local_priority = BooleanField("Сначала в выбранном городе/радиусе", default=True, render_kw ={'checked':''})
    submit = SubmitField("Скачать данные")
     