from flask import Blueprint, render_template, current_app
from models.product import Product
from models.category import Category

main = Blueprint('main', __name__)

@main.route('/')
def index():
    featured_products = Product.query.limit(6).all()
    categories = Category.query.all()
    # Deals du jour dynamiques (ex : produits en promo ou au hasard)
    deals_of_the_day = Product.query.order_by(Product.id.desc()).limit(6).all()
    # Suggestions personnalisées (autres produits, ici par défaut les 6 suivants)
    suggestions = Product.query.order_by(Product.id.asc()).limit(6).all()
    return render_template('pages/index.html', 
                         featured_products=featured_products,
                         categories=categories,
                         deals_of_the_day=deals_of_the_day,
                         suggestions=suggestions)

@main.route('/about')
def about():
    return render_template('pages/about.html')

@main.route('/contact')
def contact():
    return render_template('pages/contact.html')

@main.route('/terms')
def terms():
    return render_template('pages/terms.html')

@main.route('/privacy')
def privacy():
    return render_template('pages/privacy.html')

@main.route('/legal')
def legal():
    return render_template('pages/legal.html')

@main.route('/confidentialite')
def confidentialite():
    return render_template('pages/confidentialite.html')

@main.route('/template-test')
def template_test():
    return render_template('pages/template_test.html')
