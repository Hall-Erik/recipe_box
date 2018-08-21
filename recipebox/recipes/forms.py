from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, SubmitField, IntegerField,
					HiddenField)
from wtforms.validators import DataRequired, Regexp

class RecipeForm(FlaskForm):
	title = StringField('Name', validators=[DataRequired()])
	description = StringField('Description')
	cook_time = IntegerField('Cook Time', validators=[DataRequired()])
	servings = StringField('Number of Servings',
						validators=[DataRequired(), Regexp(r'(^\d+$)|(^[\d]+-[\d]+$)')])
	picture = HiddenField('Recipe Photo')
	ingredients = TextAreaField('Ingredients')
	directions = TextAreaField('Directions')

class CreateRecipeForm(RecipeForm):	
	submit = SubmitField('Create')

class EditRecipeForm(RecipeForm):
	submit = SubmitField('Update')