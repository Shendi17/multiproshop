from flask import Blueprint, render_template, current_app
from models.product import Product
from models.category import Category

main = Blueprint('main', __name__)

@main.route('/')
def index():
    featured_products = Product.query.limit(6).all()
    categories = Category.query.all()
    return render_template('index.html', 
                         featured_products=featured_products,
                         categories=categories)

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')

@main.route('/terms')
def terms():
    return render_template('terms.html')

@main.route('/privacy')
def privacy():
    return render_template('privacy.html')
