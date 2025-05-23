from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.product import Product
from models.category import Category
from sqlalchemy import or_

products = Blueprint('products', __name__)

@products.route('/')
def list_products():
    page = request.args.get('page', 1, type=int)
    per_page = 12
    sort_by = request.args.get('sort', 'name')
    category_id = request.args.get('category', type=int)
    
    query = Product.query
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if sort_by == 'price_asc':
        query = query.order_by(Product.price.asc())
    elif sort_by == 'price_desc':
        query = query.order_by(Product.price.desc())
    else:
        query = query.order_by(Product.name.asc())
    
    products = query.paginate(page=page, per_page=per_page)
    categories = Category.query.all()
    
    return render_template('pages/list.html',
                         products=products,
                         categories=categories,
                         current_category=category_id,
                         current_sort=sort_by)

@products.route('/search')
def search():
    query = request.args.get('q', '')
    if query:
        search_query = f"%{query}%"
        products = Product.query.filter(
            or_(
                Product.name.ilike(search_query),
                Product.description.ilike(search_query)
            )
        ).all()
    else:
        products = []
    
    return render_template('pages/search.html',
                         products=products,
                         query=query)

@products.route('/category/<int:category_id>')
def category_products(category_id):
    category = Category.query.get_or_404(category_id)
    products = Product.query.filter_by(category_id=category_id).all()
    return render_template('pages/category_products.html',
                         category=category,
                         products=products)

@products.route('/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    related_products = Product.query.filter_by(category_id=product.category_id).limit(4).all()
    return render_template('pages/product_detail.html',
                         product=product,
                         related_products=related_products)
