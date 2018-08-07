from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def error_404(error):
	pass

@errors.app_errorhandler(403)
def error_403(error):
	pass

@errors.app_errorhandler(500)
def error_500(error):
	pass