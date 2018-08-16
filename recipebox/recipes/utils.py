import recipebox.utils as utils

def save_picture(form_picture):
	return utils.save_picture(form_picture=form_picture, path='static/recipe_pics', output_size=(200,200))
