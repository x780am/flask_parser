from flask import render_template, redirect, abort, url_for, request, g
from flask_login import current_user, login_required
from app.help import bp
from app.help import json_data 

@bp.route('/', methods=['GET'])
def index():
    return redirect(url_for('help.block', active_block='faq'))

@bp.route('/<active_block>', methods=['GET'])
def block(active_block):    
    active_block_array = json_data.get_active_block_array()
    faqs = json_data.get_faq(support_email=g.support_email)
    for active_block_a in active_block_array:
        if active_block_a['id'] == active_block:
            active_block_a['show'] = True
            return render_template("help/help.html", blocks=active_block_array, faqs=faqs)    
    abort(404)

