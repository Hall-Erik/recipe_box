from recipebox import create_app, db
from recipebox.models import User, Recipe, Ingredient, Direction
from flask_alembic import Alembic

app = create_app()
app.app_context().push()

alembic = Alembic(app)

alembic.revision('made changes')

input("Press Enter to apply migration...")

alembic.upgrade()