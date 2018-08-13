from flask import (Blueprint, render_template, flash,
					redirect, url_for, abort)
from flask_login import current_user, login_required
from recipebox import db
from recipebox.recipes.forms import CreateRecipeForm
from recipebox.recipes.utils import save_picture
from recipebox.models import Recipe, Ingredient, Direction

recipes = Blueprint('recipes', __name__)

@recipes.route('/recipes/new', methods=['POST', 'GET'])
@login_required
def create_recipe():
	form = CreateRecipeForm()
	if form.validate_on_submit():
		recipe = Recipe(title=form.title.data, description=form.description.data, user_id=current_user.id)
		if form.picture.data:
			picture = save_picture(form.picture.data)
			recipe.image_file = picture
		db.session.add(recipe)
		db.session.commit()
		for ingredient in form.ingredients:
			i = Ingredient(content=ingredient.data, recipe=recipe)
			db.session.add(i)
			db.session.commit()
		for direction in form.directions:
			d = Direction(content=direction.data, recipe=recipe)
			db.session.add(d)
			db.session.commit()
		flash('Your recipe has been added!', 'success')
		return redirect(url_for('main.home'))
	print(form.errors)
	return render_template('recipes/create_recipe.html', title="Create Recipe", form=form)

@recipes.route('/recipe/<int:recipe_id>')
def recipe(recipe_id):
	recipe = Recipe.query.get_or_404(recipe_id)
	return render_template('recipes/recipe.html', title=recipe.title, recipe=recipe)

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