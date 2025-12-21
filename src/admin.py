import os
from flask_admin import Admin
from models import db, User, Characters, FavCharacters, Planets, FavPlanets, Starships, FavStarships
from flask_admin.contrib.sqla import ModelView


class UserModelView(ModelView):
    column_auto_select_related = True  # Cargar las relaciones
    column_list = ['id', 'email', 'password', 'is_active',
                   'favorites_char', 'favorites_plan', 'favorites_star']

class CharactersModelView(ModelView):
    column_auto_select_related = True  # Cargar las relaciones
    column_list = ['id', 'name', 'height', 'weigth', 'favorites_by_char']

class FavCharactersModelView(ModelView):
    column_auto_select_related = True
    column_list = ['id', 'user_id', 'users_c', 'character_id', 'people']

class PlanetsModelView(ModelView):
    column_auto_select_related = True
    column_list = ['id', 'name', 'diameter', 'orbital_period', 'favorites_by_plan']

class FavPlanetsModelView(ModelView):
    column_auto_select_related = True
    column_list = ['id', 'user_id', 'users_p', 'planet_id', 'astros']

class StarshipsModelView(ModelView):
    column_auto_select_related = True
    column_list = ['id', 'name', 'passengers', 'cargo_capacity', 'favorites_by_star']

class FavStarshipsModelView(ModelView):
    column_auto_select_related = True
    column_list = ['id', 'user_id', 'users_s', 'starship_id', 'naves']

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(CharactersModelView(Characters, db.session))
    admin.add_view(FavCharactersModelView(FavCharacters, db.session))
    admin.add_view(PlanetsModelView(Planets, db.session))
    admin.add_view(FavPlanetsModelView(FavPlanets, db.session))
    admin.add_view(StarshipsModelView(Starships, db.session))
    admin.add_view(FavStarshipsModelView(FavStarships, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))
