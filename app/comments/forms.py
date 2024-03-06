from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from wtforms.widgets import TextArea

class MyBaseForm(FlaskForm):
    class Meta:
        locales = ['ru']
        def get_translations(self, form):
            return super(FlaskForm.Meta, self).get_translations(form)

    
class CommentsAddForm(MyBaseForm):
    name = StringField(label='Ваше имя',validators=[DataRequired()], render_kw={"placeholder": "Введите Ваше имя"})
    email = StringField(label='Email',validators=[DataRequired(), Email()], render_kw={"placeholder": "Введите email для ответа"})
    message = StringField(label='Текст отзыва', widget=TextArea(), validators=[DataRequired()], render_kw={"placeholder": "Напишите Ваш отзыв"}) 
    # submit = SubmitField('<i class="far fa-envelope"></i> Отправить')
    submit = SubmitField('Отправить')
    
class EditCommentForm(MyBaseForm):
    text = StringField(label='', widget=TextArea(), validators=[DataRequired()]) 
    id = StringField(label='id',validators=[DataRequired()], render_kw={"type":"hidden"})
    answer = StringField(label='answer',validators=[DataRequired()], render_kw={"type":"hidden"})
    comment_text = StringField(label='comment_text',validators=[DataRequired()], render_kw={"type":"hidden"})
    email = StringField(label='email',validators=[DataRequired()], render_kw={"type":"hidden"})    
    # submit = SubmitField('<i class="far fa-envelope"></i> Отправить')
    submit = SubmitField('Сохранить', render_kw={"data-bs-dismiss":"modal"})    
    