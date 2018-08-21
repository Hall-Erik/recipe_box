import secrets, os

def rand_picture_name(filename):
	rand_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(filename)
	return rand_hex + f_ext