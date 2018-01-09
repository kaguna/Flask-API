# creates the user, categories and recipes tables schema

from app import db

# import the db connection from the app/__init__.py


class Users(db.Model):
    """ This class represents the users table"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(80))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())
    # categories = db.relationship(
    #     'Categories', order_by='categories.id', cascade="all, delete-orphan")

    def __init__(self, email):
        """initialize with user email."""
        self.email = email

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Users.query.all()

    def __repr__(self):
        return "<Users: {}>".format(self.email)


class Categories(db.Model):
    """ This class represents the recipe categories table"""
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), unique=True)
    users_id = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())
    # recipes = db.relationship(
    #     'Recipes', order_by='recipes.id', cascade="all, delete-orphan")

    def __init__(self, category_name, users_id):
        """initialize with user email."""
        self.category_name = category_name
        self.users_id = users_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Categories.query.all()

    def __repr__(self):
        return "<Categories: {}>".format(self.category_name)


class Recipes(db.Model):
    """ This class represents the recipes table"""

    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(100), unique=True)
    recipe_description = db.Column(db.String(255))
    # category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())

    def __init__(self, recipe_name):
        """initialize with user email."""
        self.recipe_name = recipe_name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Recipes.query.all()

    def __repr__(self):
        return "<Recipes: {}>".format(self.recipe_name)
