from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    pizzas = db.relationship('RestaurantPizza', back_populates='restaurant')

    @validates('name')
    def validate_name(self, key, name):
        assert name.strip(), "Name can't be empty"
        return name

    @validates('address')
    def validate_address(self, key, address):
        assert address.strip(), "Address can't be empty"
        return address

    def __repr__(self):
        return f'<Restaurant {self.name}>'

class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    restaurants = db.relationship('RestaurantPizza', back_populates='pizza')

    @validates('name')
    def validate_name(self, key, name):
        assert name.strip(), "Name can't be empty"
        return name

    @validates('ingredients')
    def validate_ingredients(self, key, ingredients):
        assert ingredients.strip(), "Ingredients can't be empty"
        return ingredients

    def __repr__(self):
        return f'<Pizza {self.name}>'

class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizzas'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)

    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    restaurant = db.relationship('Restaurant', back_populates='pizzas')

    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    pizza = db.relationship('Pizza', back_populates='restaurants')

    @validates('price')
    def validate_price(self, key, price):
        assert 1 <= price <= 30, "Price must be between 1 and 30"
        return price

    def __repr__(self):
        return f'<RestaurantPizza {self.id}>'
