from flask_login import UserMixin
from grocery_app.extensions import db
from grocery_app.utils import FormEnum

class ItemCategory(FormEnum):
    """Categories of grocery items."""
    PRODUCE = 'Produce'
    DELI = 'Deli'
    BAKERY = 'Bakery'
    PANTRY = 'Pantry'
    FROZEN = 'Frozen'
    OTHER = 'Other'


class GroceryStore(db.Model):
    """Grocery Store model."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    items = db.relationship('GroceryItem', back_populates='store')
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User', back_populates='stores')

    def __str__(self):
        return f'{self.title}'
    
class GroceryItem(db.Model):
    """Grocery Item model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    category = db.Column(db.Enum(ItemCategory), default=ItemCategory.OTHER)
    photo_url = db.Column(db.String)
    store_id = db.Column(
        db.Integer, db.ForeignKey('grocery_store.id'), nullable=False)
    store = db.relationship('GroceryStore', back_populates='items')
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User', back_populates='items')
    users_shopping_list = db.relationship(
        'User', secondary='user_item', back_populates="shopping_list_items")

class User(UserMixin, db.Model):
    """User Model"""
    # id, username, password
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    items = db.relationship('GroceryItem', back_populates='created_by')
    stores = db.relationship('GroceryStore', back_populates='created_by')
    shopping_list_items = db.relationship(
        'GroceryItem', secondary='user_item', back_populates="users_shopping_list")
    
shopping_list_table = db.Table('user_item',
    db.Column('grocery_item_id', db.Integer, db.ForeignKey('grocery_item.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True))
