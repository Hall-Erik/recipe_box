from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, FieldList, SubmitField
from wtforms.validators import DataRequired

class CreateRecipeForm(FlaskForm):
	title = StringField('Name', validators=[DataRequired()])
	description = StringField('Description')
	picture = FileField('Recipe Photo', 
							validators=[FileAllowed(['jpg', 'png'])])
	ingredients = FieldList(StringField('Ingredients'), min_entries=1)
	directions = FieldList(StringField('Directions'), min_entries=1)
	submit = SubmitField('Submit')

class EditRecipeForm(FlaskForm):
	title = StringField('Name', validators=[DataRequired()])
	description = StringField('Description')
	picture = FileField('Change Recipe Photo', 
							validators=[FileAllowed(['jpg', 'png'])])
	ingredients = FieldList(StringField('Ingredients'), min_entries=1)
	directions = FieldList(StringField('Directions'), min_entries=1)
	submit = SubmitField('Update')