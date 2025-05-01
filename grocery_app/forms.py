from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, DecimalField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL
from grocery_app.models import GroceryStore, ItemCategory

class GroceryStoreForm(FlaskForm):
    """Form for adding/updating a GroceryStore."""
    title = StringField('Grocery Store Title',
                validators=[
                    DataRequired(),
                    Length(min=5, max=80, message="Your title needs to be between 5 and 80 characters")
                ])
    address = StringField('Address',
                validators=[
                    DataRequired(),
                    Length(min=3, max=80, message="Address must be between 3 and 80 chars")
                ])
    submit = SubmitField('Submit')

class GroceryItemForm(FlaskForm):
    """Form for adding/updating a GroceryItem."""
    name = StringField('Item',
            validators=[
                DataRequired(),
                Length(min=3, max=80, message="Item name needs to be between 3 and 80 chars")
            ])
    
    price = DecimalField('Price', validators=[DataRequired()], places=2)
    category = SelectField('Category', choices=ItemCategory.choices())
    photo_url = StringField('Photo URL')
    store = QuerySelectField('Store', query_factory=lambda: GroceryStore.query)    
    submit = SubmitField('Submit')
