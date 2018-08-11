from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, SubmitField
from wtforms.validators import DataRequired

class IngredientForm(FlaskForm):
	content = StringField('Ingredient')

class CreateRecipeForm(FlaskForm):
	title = StringField('Name', validators=[DataRequired()])
	description = StringField('Description')
	ingredients = FieldList(StringField('Ingredients'), min_entries=1)
	directions = FieldList(StringField('Directions'), min_entries=1)
	submit = SubmitField('Submit')