from flask import render_template, url_for, request, current_app, jsonify, g
from flask_login import current_user
from app.comments import bp
from app.comments.forms import CommentsAddForm, EditCommentForm
from app.comments.models import Comments
from app.utils import admin_required
from app.comments.email import send_comment_new_to_admin, send_comment_answer_to_client


@bp.route('/', methods=['GET'])
def index():
    commentAdd_form = CommentsAddForm() 
    EditComment_form = EditCommentForm() 
    if not current_user.is_anonymous:
        commentAdd_form.email.data = current_user.login
    page = request.args.get('page', 1, type=int)  
    public_view = False if current_user.is_admin else True
    comments = Comments().get_comments(page=page, per_page=current_app.config['COMMENTS_PER_PAGE'], public_view=public_view)
    if comments and 'comments' in comments and comments['comments']:
        prev_url = url_for('comments.index', page=page-1) if comments['has_prev'] else None 
        next_url = url_for('comments.index', page=page+1) if comments['has_next'] else None
        return render_template('comments/comments.html', comments=comments['comments'], next_url=next_url, prev_url=prev_url, commentAdd_form=commentAdd_form, EditComment_form=EditComment_form)
    else:
        return render_template('comments/comments.html', comments=None, next_url=None, prev_url=None, commentAdd_form=commentAdd_form, EditComment_form=EditComment_form)    

@bp.route('/add', methods=['POST'])
def add():
    commentAdd_form=CommentsAddForm()
    if commentAdd_form.validate():
        Comments().comment_add( name=commentAdd_form.name.data, 
                                email=commentAdd_form.email.data, 
                                text=commentAdd_form.message.data,
                                ip=g.ip_address)
        send_comment_new_to_admin(name=commentAdd_form.name.data, 
                                email=commentAdd_form.email.data, 
                                message=commentAdd_form.message.data)
        return 'Спасибо. Ваше сообщение будет опубликовано после проверки модератором.'
    return jsonify(commentAdd_form.errors), 400

@bp.route('/answer', methods=['POST'])
@admin_required
def answer():
    EditComment_form = EditCommentForm() 
    if EditComment_form.validate():
        Comments().comment_add( text=EditComment_form.text.data,
                                answer=EditComment_form.id.data,
                                ip=g.ip_address,
                                admin=1)
        send_comment_answer_to_client(email=EditComment_form.email.data, 
                                      comment_text=EditComment_form.comment_text.data,
                                      answer_text=EditComment_form.text.data)
        return 'Спасибо за ответ'
    return jsonify(EditComment_form.errors), 400
    
@bp.route('/public', methods=['POST'])
@admin_required
def public():
    if 'id' in request.json:
        id = request.json['id']
        if id > 0: 
            public = request.json['public'] if 'public' in request.json else 0
            if Comments().comment_public(id=id, public=public):
                return 'ok', 200
    return 'Ошибка', 400

@bp.route('/delete', methods=['POST'])
@admin_required
def delete():
    if 'id' in request.json:
        id = request.json['id']
        if id > 0: 
            if Comments().comment_delete(id=id):
                return 'ok', 200
    return 'Ошибка', 400

@bp.route('/edit', methods=['POST'])
@admin_required
def edit():
    EditComment_form = EditCommentForm() 
    
    if Comments().comment_edit(id=EditComment_form.id.data, 
                                text=EditComment_form.text.data):
        return 'ok', 200
    return 'Ошибка', 400