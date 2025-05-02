from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime

from flask_login import current_user, login_required
from grocery_app.models import GroceryStore, GroceryItem
from grocery_app.forms import GroceryStoreForm, GroceryItemForm

# Import app and db from events_app package so that we can run app
from grocery_app.extensions import app, db

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    all_stores = GroceryStore.query.all()
    print(all_stores)
    return render_template('home.html', all_stores=all_stores)

@main.route('/new_store', methods=['GET', 'POST'])
@login_required
def new_store():
    form = GroceryStoreForm()
    
    if form.validate_on_submit():
        create_store = GroceryStore(
            title=form.title.data,
            address=form.address.data,
            created_by=current_user,
        )
        
        db.session.add(create_store)
        db.session.commit()
        
        flash(f"{create_store.title} created successfully")
        return redirect(url_for('main.homepage'))
    return render_template('new_store.html', form=form)

@main.route('/new_item', methods=['GET', 'POST'])
@login_required
def new_item():
    # Create a GroceryItemForm
    form = GroceryItemForm()
    
    if form.validate_on_submit():
        create_item = GroceryItem(
            name = form.name.data,
            price = form.price.data,
            category = form.category.data,
            photo_url = form.photo_url.data,
            store = form.store.data,
            created_by=current_user
        )
        
        db.session.add(create_item)
        db.session.commit()
        
        flash(f"{create_item.name} created successfully")
        return redirect(url_for('main.item_detail', item_id = create_item.id))
    return render_template('new_item.html', form=form)

@main.route('/store/<store_id>', methods=['GET', 'POST'])
@login_required
def store_detail(store_id):
    store = GroceryStore.query.get_or_404(store_id)
    form = GroceryStoreForm(obj=store)
    
    if form.validate_on_submit():
        form.populate_obj(store)
        
        db.session.commit()
        
        flash(f"{store.title} was updated successfully")
        return redirect(url_for('main.store_detail', store_id = store.id))
    return render_template('store_detail.html', store=store, form=form)

@main.route('/item/<item_id>', methods=['GET', 'POST'])
@login_required
def item_detail(item_id):
    item = GroceryItem.query.get_or_404(item_id)
    form = GroceryItemForm(obj=item)
    
    if form.validate_on_submit():
        form.populate_obj(item)
        
        db.session.commit()
        
        flash(f"{item.name} was updated successfully")
        return redirect(url_for('main.item_detail', item_id = item.id))

    return render_template('item_detail.html', item=item, form=form)

@main.route('/shopping_list', methods=['GET'])
@login_required
def shopping_list():
    """ Display the current user's shopping list """
    return render_template('shopping_list.html', shopping_list_items=current_user.shopping_list_items)

@main.route('/add_shopping/<item_id>', methods=['POST'])
@login_required
def add_to_shopping_list(item_id):
    """ Adds item to current user's shopping list """
    shop_item = GroceryItem.query.get(item_id)
    
    if shop_item not in current_user.shopping_list_items:
        current_user.shopping_list_items.append(shop_item)
        db.session.commit()
        
        flash(f"You added {shop_item.name} to your shopping list")
        
    return redirect(url_for('main.item_detail', item_id = item_id))

@main.route('/remove_shopping/<item_id>', methods=['POST'])
@login_required
def remove_to_shopping_list(item_id):
    """ Removes item to current user's shopping list"""
    shop_item = GroceryItem.query.get(item_id)
    
    if shop_item in current_user.shopping_list_items:
        current_user.shopping_list_items.remove(shop_item)
        db.session.commit()
        
        flash(f"You removed {shop_item.name} from your shopping list")
    
    return redirect(url_for('main.item_detail', item_id = item_id))
