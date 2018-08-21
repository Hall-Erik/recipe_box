from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Regexp

class RecipeForm(FlaskForm):
	title = StringField('Name', validators=[DataRequired()])
	description = StringField('Description')
	cook_time = IntegerField('Cook Time', validators=[DataRequired()])
	servings = StringField('Number of Servings (e.g. 5, 7-8)',
						validators=[DataRequired(), Regexp(r'(^\d+$)|(^[\d]+-[\d]+$)')])
	picture = FileField('Recipe Photo', 
						validators=[FileAllowed(['jpg', 'png'])])
	ingredients = TextAreaField('Ingredients')
	directions = TextAreaField('Directions')

class CreateRecipeForm(RecipeForm):	
	submit = SubmitField('Create')

class EditRecipeForm(RecipeForm):
	submit = SubmitField('Update')