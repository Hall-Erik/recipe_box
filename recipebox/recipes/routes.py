from flask import (Blueprint, render_template, flash,
					redirect, url_for, abort)
from flask_login import current_user, login_required
from recipebox import db
from recipebox.recipes.forms import CreateRecipeForm, EditRecipeForm
from recipebox.models import Recipe

recipes = Blueprint('recipes', __name__)

@recipes.route('/recipes/new', methods=['POST', 'GET'])
@login_required
def create_recipe():
	form = CreateRecipeForm()
	if form.validate_on_submit():
		recipe = Recipe(title=form.title.data,
						description=form.description.data,
						cook_time=form.cook_time.data,
						servings=form.servings.data,
						ingredients=form.ingredients.data,
						directions=form.directions.data,
						user_id=current_user.id)
		if form.picture.data and form.picture.data != url_for('static', filename='img/default.png'):
			recipe.image_file = form.picture.data
		db.session.add(recipe)
		db.session.commit()
		flash('Your recipe has been added!', 'success')
		return redirect(url_for('main.home'))
	recipe_picture = url_for('static', filename='img/default.png')
	return render_template('recipes/create_edit_recipe.html',
						title="Create Recipe",
						legend="Add a recipe!",
						recipe_picture=recipe_picture,
						form=form)

@recipes.route('/recipe/<int:recipe_id>')
def recipe(recipe_id):
	recipe = Recipe.query.get_or_404(recipe_id)
	return render_template('recipes/recipe.html', title=recipe.title, recipe=recipe)

@recipes.route('/recipe/<int:recipe_id>/edit', methods=['POST', 'GET'])
@login_required
def edit_recipe(recipe_id):
	recipe = Recipe.query.get_or_404(recipe_id)
	if recipe.author != current_user:
		abort(403)
	form = EditRecipeForm(obj=recipe)
	if form.validate_on_submit():
		recipe.title = form.title.data
		recipe.description = form.description.data
		recipe.cook_time = form.cook_time.data
		recipe.servings = form.servings.data
		recipe.ingredients = form.ingredients.data
		recipe.directions = form.directions.data
		if form.picture.data and recipe.image_file != form.picture.data:
			recipe.image_file = form.picture.data
		db.session.commit()
		return redirect(url_for('recipes.recipe', recipe_id=recipe.id))
	recipe_picture = recipe.get_image_url()
	print(recipe_picture)
	return render_template('recipes/create_edit_recipe.html',
						title="Update Recipe",
						legend="Edit recipe!",
						recipe_picture=recipe_picture,
						form=form)
	
@recipes.route('/recipe/<int:recipe_id>/delete', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
	recipe = Recipe.query.get_or_404(recipe_id)
	if recipe.author != current_user:
		abort(403)
	db.session.delete(recipe)
	db.session.commit()
	flash('Your recipe has been deleted!', 'success')
	return redirect(url_for('main.home'))