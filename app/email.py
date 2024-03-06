from threading import Thread
from flask import current_app
from flask_mail import Message
from app import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, html_body, sender='', recipient='', text_body=''):
    if not sender:
        sender = current_app.config['ADMIN']
    if not recipient:
        recipient = current_app.config['ADMIN']
    msg = Message(subject, sender=sender, recipients=[recipient])
    if text_body: 
        msg.body = text_body
    else:
        msg.body = html_body
    msg.html = html_body
    Thread(target=send_async_email,
           args=(current_app._get_current_object(), msg)).start()
    
    
#     // запишем в БД
            # $ins_array=array(
            #             'sendto' => $SendTo,
            #             'bodymail' => $BodyMail,
            #             'subject' => $Subject,
            #             'mail_type'=>$mail_type
            #             );

            # $db->insert('log_mail_send', $ins_array);
            # unset($ins_array,$Error,$BodyMail);
    