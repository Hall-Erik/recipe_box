from flask_wtf import FlaskForm
from wtforms import StringField, FormField, FieldList, SubmitField
from wtforms.validators import DataRequired

class IngredientForm(FlaskForm):
	content = StringField('Ingredient')

class CreateRecipeForm(FlaskForm):
	title = StringField('Name', validators=[DataRequired()])
	description = StringField('Description')

	ingredients = FieldList(StringField('Ingredient'), min_entries=1)

	submit = SubmitField('Submit')