from flask import (
	render_template,
	Blueprint,
	request,
	g,
	redirect,
	url_for)
from recipebox.models import Recipe
import os, json, boto3
from recipebox.utils import rand_picture_name
from recipebox.main.forms import SearchForm

main = Blueprint('main', __name__)

@main.before_app_request
def before_app_request():
	g.search_form = SearchForm()

@main.route('/')
@main.route('/home')
def home():
	recipes = Recipe.query.all()
	return render_template("home.html", recipes=recipes)

@main.route('/search')
def search():
	if not g.search_form.validate():
		return redirect(url_for('main.home'))
	recipes = Recipe.query.all()
	return render_template('home.html', title='Search', recipes=recipes)

@main.route('/about')
def about():
	return render_template("about.html", title="About")

@main.route('/sign_s3/')
def sign_s3():
	S3_BUCKET = os.environ.get('S3_BUCKET_NAME')

	file_name = rand_picture_name(request.args.get('file_name'))
	file_type = request.args.get('file_type')

	s3 = boto3.client('s3')

	presigned_post = s3.generate_presigned_post(
		Bucket = S3_BUCKET,
		Key = file_name,
		Fields = {"acl": "public-read", "Content-Type": file_type},
		Conditions = [
			{"acl": "public-read"},
			{"Content-Type": file_type}
		],
		ExpiresIn = 3600
	)

	return json.dumps({
		'data': presigned_post,
		'url': 'https://%s.s3.us-west-1.amazonaws.com/%s' % (S3_BUCKET, file_name)
	})