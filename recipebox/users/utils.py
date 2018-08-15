import secrets, os
from PIL import Image
from flask import current_app, url_for
from flask_mail import Message
from recipebox import mail

def save_picture(form_picture):
	rand_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_filename = rand_hex + f_ext
	picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_filename)
	output_size = (150, 150)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)
	return picture_filename

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
