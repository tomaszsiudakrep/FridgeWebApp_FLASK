from datetime import datetime

import flask_login
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy.sql.functions import user

from .models import Note, Group, Product, User, Unit, Ingredient
from website import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) <= 1:
            flash('Note is too short', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added', category='success')

    return render_template("home.html", user=current_user)


@views.route('/fridge_status', methods=['GET', 'POST'])
@login_required
def ingredient():
    products = Product.query.all()
    units = [e.value for e in Unit]
    ingredients = Ingredient.query.all()

    if request.method == 'POST':
        unit = request.form.get('unit')
        product_id = request.form.get('product')
        expiration_date = request.form.get('expiration_date')
        expiration_date = datetime.strptime(expiration_date, '%Y-%m-%d').date()

        if unit == 'Choose...':
            flash('Select unit', category='error')
        elif product == 'Choose...':
            flash('Select product', category='error')
        else:
            new_ingredient = Ingredient(product_id=product_id, unit=unit, expiration_date=expiration_date)
            db.session.add(new_ingredient)
            db.session.commit()
            flash('Ingredient added', category='success')

    return render_template("ingredient.html", user=current_user, products=products, units=units, ingredients=ingredients)


@views.route('/group', methods=['GET', 'POST'])
@login_required
def product_group():
    if request.method == 'POST':
        group = request.form.get('group')

        if len(group) <= 1:
            flash('Group is too short', category='error')
        else:
            new_group = Group(name=group, user_id=current_user.id)
            db.session.add(new_group)
            db.session.commit()
            flash('Group added', category='success')

    return render_template("group.html", user=current_user)


@views.route('/product', methods=['GET', 'POST'])
@login_required
def product():
    groups = Group.query.all()

    products = []
    for group in groups:
        products += [(group, product) for product in group.product]

    if request.method == 'POST':
        product = request.form.get('product')
        group = request.form.get('group')
        expiration_date = request.form.get('expiration_date')
        expiration_date = datetime.strptime(expiration_date, '%Y-%m-%d').date()
        # expiration_date = datetime.strptime(expiration_date, '%Y-%m-%dT%H:%M')
        if len(product) <= 1:
            flash('Product is too short', category='error')
        else:
            new_product = Product(name=product, group_id=group, expiration_date=expiration_date)
            db.session.add(new_product)
            db.session.commit()
            flash('Product added', category='success')

    return render_template("product.html", user=current_user, groups=groups, products=products)


@views.route('/expiration', methods=['GET'])
@login_required
def expiration():
    products = Product.query.order_by(Product.expiration_date.asc()).all()

    return render_template("expiration.html", user=current_user, products=products)


@views.route('/group/<int:group_id>', methods=['GET'])
def get_group(group_id):
    group = Group.query.get_or_404(group_id)
    return jsonify({'id': group.id, 'name': group.name, 'date': group.date.isoformat()})

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route('/delete-group', methods=['POST'])
def delete_group():
    group = json.loads(request.data)
    groupId = group['groupId']
    group = Group.query.get(groupId)
    if group:
        if group.user_id == current_user.id:
            db.session.delete(group)
            db.session.commit()

    return jsonify({})


@views.route('/delete-product', methods=['POST'])
def delete_product():
    product = json.loads(request.data)
    productId = product['productId']
    product = Product.query.get(productId)
    user_id = db.session.query(User.id).join(Group).join(Product).filter(Product.id == productId).scalar()
    if product:
        if user_id == current_user.id:
            db.session.delete(product)
            db.session.commit()

    return jsonify({})

