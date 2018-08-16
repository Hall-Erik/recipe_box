import secrets, os
from PIL import Image
from flask import current_app

def save_picture(form_picture, path, output_size):
	rand_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_filename = rand_hex + f_ext
	picture_path = os.path.join(current_app.root_path, path, picture_filename)
	output_size = output_size
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)
	return picture_filename