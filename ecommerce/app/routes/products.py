import boto3
import logging
import time


from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from app.models import db, Product
from app import limiter
from app import Config

products = Blueprint('products', __name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_products_internal():
    logging.info('Querying DB...')
    products = Product.query.all()
    logging.info('Done querying.')

    return [{
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'price': p.price,
        'stock': p.stock,
        'image_url': p.image_url
    } for p in products]

@products.route('/browser/inventory', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def inventory_browser():
    return render_template('inventory.html')

@products.route('/browser/products', methods=['GET'])
@limiter.limit("5 per minute")
def get_products_browser():
    return render_template('base.html', products=get_products_internal())

@products.route('/products', methods=['GET'])
@limiter.limit("5 per minute")
def get_products():
    return jsonify(get_products_internal())

@products.route('/checkout', methods=['POST'])
@login_required
@limiter.limit("5 per minute")
def checkout():
    logging.info('Creating DynamoDB resource and writing to table...')
    dynamodb = boto3.resource('dynamodb',
        region_name=Config.REGION_NAME,
        aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
    )

    table = dynamodb.Table('Orders')
    
    for product in get_products_internal():
        item = {
            'order_id': str(time.process_time_ns()),
            'name': product['name'],
            'user_id': current_user.id,
            'user_email': current_user.email,
        }
        table.put_item(Item=item)

    logging.info('Dynamo updated.')

    logging.info('Deleting from DB...')
    db.session.query(Product).delete()
    db.session.commit()
    logging.info('Done deleting')

    return jsonify({'message': 'Checkout done'}), 201

@products.route('/products', methods=['POST'])
@login_required
@limiter.limit("5 per minute")
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
@limiter.limit("5 per minute")
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
@limiter.limit("5 per minute")
def delete_product(id):
    logging.info('Querying DB...')
    product = Product.query.get_or_404(id)
    logging.info('Done querying.')

    logging.info('Deleting from DB...')
    db.session.delete(product)
    db.session.commit()
    logging.info('Done deleting.')

    return jsonify({'message': 'Product deleted'})