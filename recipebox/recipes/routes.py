from flask import (Blueprint, render_template, flash,
					redirect, url_for, abort)
from flask_login import current_user, login_required
from recipebox import db
from recipebox.recipes.forms import CreateRecipeForm, EditRecipeForm
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
		if form.picture.data:
			picture = save_picture(form.picture.data)
			recipe.image_file = picture
		
		db_ing = [ingredient.content for ingredient in recipe.ingredients]
		form_ing = [ingredient.data for ingredient in form.ingredients if ingredient.data != ""]
		old_ing = set(db_ing) - set(form_ing)
		new_ing = set(form_ing) - set(db_ing)

		for ingredient in recipe.ingredients:
			if ingredient.content in old_ing:
				db.session.delete(ingredient)

		for ingredient in new_ing:
			i = Ingredient(content=ingredient, recipe=recipe)
			db.session.add(i)

		db_dir = [direction.content for direction in recipe.directions]
		form_dir = [direction.data for direction in form.directions if direction.data != ""]
		old_dir = set(db_dir) - set(form_dir)
		new_dir = set(form_dir) - set(db_dir)

		for direction in recipe.directions:
			if direction.content in old_dir:
				db.session.delete(direction)

		for direction in new_dir:
			d = Direction(content=direction, recipe=recipe)
			db.session.add(d)
		
		# db.session.add(recipe)
		db.session.commit()
		return redirect(url_for('recipes.recipe', recipe_id=recipe.id))
	# form.title.data = recipe.title
	# form.description.data = recipe.description
	# form.ingredients = recipe.ingredients

	return render_template('recipes/edit_recipe.html', title="Update Recipe", form=form, ing_len=len(recipe.ingredients), dir_len=len(recipe.directions))