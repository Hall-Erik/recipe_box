from flask import url_for
from flask_mail import Message
from recipebox import mail
import recipebox.utils as utils

def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Password Reset Request Do Not Reply',
			sender='noreply@recipebox.com',
			recipients=[user.email])
	msg.body = f'''To reset your password, visit the link below:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, ignore this email and nothing will happen.
'''
	mail.send(msg)
