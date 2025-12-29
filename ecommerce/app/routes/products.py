import logging

from flask import Blueprint, request, jsonify
from flask_login import login_required
from app.models import db, Product

products = Blueprint('products', __name__)

@products.route('/products', methods=['GET'])
def get_products():
    logging.info('Querying DB...')
    products = Product.query.all()
    logging.info('Done querying.')

    return jsonify([{
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'price': p.price,
        'stock': p.stock,
        'image_url': p.image_url
    } for p in products])

@products.route('/products', methods=['POST'])
@login_required
def create_product():
    data = request.get_json()
    if {'name', 'description', 'price', 'stock', 'image_url'} != data.keys():
        return jsonify({'message': 'Error: all product fields required'}), 400

    product = Product(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        stock=data['stock'],
        image_url=data.get('image_url')
    )

    logging.info('Writing to DB...')
    db.session.add(product)
    db.session.commit()
    logging.info('Done writing.')

    return jsonify({'message': 'Product created'}), 201

@products.route('/products/<int:id>', methods=['PUT'])
@login_required
def update_product(id):
    logging.info('Querying DB...')
    product = Product.query.get_or_404(id)
    logging.info('Done querying.')

    data = request.get_json()
    for key, value in data.items():
        setattr(product, key, value)

    db.session.commit()
    logging.info('Done updating DB.')

    return jsonify({'message': 'Product updated'})

@products.route('/products/<int:id>', methods=['DELETE'])
@login_required
def delete_product(id):
    logging.info('Querying DB...')
    product = Product.query.get_or_404(id)
    logging.info('Done querying.')

    logging.info('Deleting from DB...')
    db.session.delete(product)
    db.session.commit()
    logging.info('Done deleting.')

    return jsonify({'message': 'Product deleted'})