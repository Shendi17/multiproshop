from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from models.role import Role
from models.category import Category

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or getattr(current_user.role, 'name', None) != 'admin':
            flash('Accès réservé aux administrateurs.')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    return render_template('pages/admin/dashboard.html')

@admin_bp.route('/users/export')
@login_required
@admin_required
def export_users():
    from models.user import User
    import csv
    from flask import Response
    users = User.query.all()
    def generate():
        data = [['ID', 'Nom', 'Email', 'Rôle', 'Date création']]
        for user in users:
            data.append([user.id, user.username, user.email, user.role.name if user.role else '', user.created_at.strftime('%d/%m/%Y')])
        for row in data:
            yield ','.join(str(cell) for cell in row) + '\n'
    return Response(generate(), mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=utilisateurs.csv"})

@admin_bp.route('/users', methods=['GET'])
@login_required
@admin_required
def users():
    from models.user import User
    search = request.args.get('search','')
    q = User.query
    if search:
        q = q.filter((User.username.ilike(f'%{search}%')) | (User.email.ilike(f'%{search}%')))
    users = q.all()
    return render_template('pages/admin/users.html', users=users, search=search)

@admin_bp.route('/users/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_user():
    roles = Role.query.all()
    if request.method == 'POST':
        from models.user import User
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role_id = request.form['role_id']
        if User.query.filter((User.username==username)|(User.email==email)).first():
            flash('Nom ou email déjà utilisé.')
            return render_template('pages/admin/user_form.html', user=None, roles=roles)
        user = User(username=username, email=email, role_id=role_id)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Utilisateur créé avec succès.')
        return redirect(url_for('admin.users'))
    return render_template('pages/admin/user_form.html', user=None, roles=roles)

@admin_bp.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    from models.user import User
    user = User.query.get_or_404(user_id)
    roles = Role.query.all()
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.role_id = request.form['role_id']
        password = request.form['password']
        if password:
            user.set_password(password)
        db.session.commit()
        flash('Utilisateur mis à jour.')
        return redirect(url_for('admin.users'))
    return render_template('pages/admin/user_form.html', user=user, roles=roles)

@admin_bp.route('/users/delete/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_user(user_id):
    from models.user import User
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        db.session.delete(user)
        db.session.commit()
        flash('Utilisateur supprimé.')
        return redirect(url_for('admin.users'))
    return render_template('pages/admin/user_delete.html', user=user)

@admin_bp.route('/products/export')
@login_required
@admin_required
def export_products():
    from models.product import Product
    import csv
    from flask import Response
    products = Product.query.all()
    def generate():
        data = [['ID', 'Nom', 'Catégorie', 'Prix', 'Stock']]
        for product in products:
            data.append([
                product.id,
                product.name,
                product.category.name if product.category else '',
                f"{product.price:.2f}",
                product.stock
            ])
        for row in data:
            yield ','.join(str(cell) for cell in row) + '\n'
    return Response(generate(), mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=produits.csv"})

@admin_bp.route('/products', methods=['GET'])
@login_required
@admin_required
def products():
    from models.product import Product
    search = request.args.get('search','')
    q = Product.query
    if search:
        q = q.join(Category, isouter=True).filter(
            (Product.name.ilike(f'%{search}%')) | (Category.name.ilike(f'%{search}%'))
        )
    products = q.all()
    return render_template('pages/admin/products.html', products=products, search=search)

@admin_bp.route('/products/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_product():
    from models.product import Product
    categories = Category.query.all()
    if request.method == 'POST':
        name = request.form['name']
        category_id = request.form['category_id']
        price = request.form['price']
        stock = request.form['stock']
        description = request.form['description']
        product = Product(name=name, category_id=category_id, price=price, stock=stock, description=description)
        db.session.add(product)
        db.session.commit()
        flash('Produit créé avec succès.')
        return redirect(url_for('admin.products'))
    return render_template('pages/admin/product_form.html', product=None, categories=categories)

@admin_bp.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(product_id):
    from models.product import Product
    product = Product.query.get_or_404(product_id)
    categories = Category.query.all()
    if request.method == 'POST':
        product.name = request.form['name']
        product.category_id = request.form['category_id']
        product.price = request.form['price']
        product.stock = request.form['stock']
        product.description = request.form['description']
        db.session.commit()
        flash('Produit mis à jour.')
        return redirect(url_for('admin.products'))
    return render_template('pages/admin/product_form.html', product=product, categories=categories)

@admin_bp.route('/products/delete/<int:product_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_product(product_id):
    from models.product import Product
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        db.session.delete(product)
        db.session.commit()
        flash('Produit supprimé.')
        return redirect(url_for('admin.products'))
    return render_template('pages/admin/product_delete.html', product=product)

@admin_bp.route('/categories/export')
@login_required
@admin_required
def export_categories():
    from models.category import Category
    import csv
    from flask import Response
    categories = Category.query.all()
    def generate():
        data = [['ID', 'Nom', 'Description']]
        for category in categories:
            data.append([
                category.id,
                category.name,
                category.description or ''
            ])
        for row in data:
            yield ','.join(str(cell) for cell in row) + '\n'
    return Response(generate(), mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=categories.csv"})

@admin_bp.route('/categories', methods=['GET'])
@login_required
@admin_required
def categories():
    from models.category import Category
    search = request.args.get('search','')
    q = Category.query
    if search:
        q = q.filter(Category.name.ilike(f'%{search}%'))
    categories = q.all()
    return render_template('pages/admin/categories.html', categories=categories, search=search)

@admin_bp.route('/categories/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_category():
    from models.category import Category
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        category = Category(name=name, description=description)
        db.session.add(category)
        db.session.commit()
        flash('Catégorie créée avec succès.')
        return redirect(url_for('admin.categories'))
    return render_template('pages/admin/category_form.html', category=None)

@admin_bp.route('/categories/edit/<int:category_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_category(category_id):
    from models.category import Category
    category = Category.query.get_or_404(category_id)
    if request.method == 'POST':
        category.name = request.form['name']
        category.description = request.form['description']
        db.session.commit()
        flash('Catégorie mise à jour.')
        return redirect(url_for('admin.categories'))
    return render_template('pages/admin/category_form.html', category=category)

@admin_bp.route('/categories/delete/<int:category_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_category(category_id):
    from models.category import Category
    category = Category.query.get_or_404(category_id)
    if request.method == 'POST':
        db.session.delete(category)
        db.session.commit()
        flash('Catégorie supprimée.')
        return redirect(url_for('admin.categories'))
    return render_template('pages/admin/category_delete.html', category=category)

@admin_bp.route('/orders/export')
@login_required
@admin_required
def export_orders():
    from models.order import Order
    import csv
    from flask import Response
    orders = Order.query.all()
    def generate():
        data = [['ID', 'Utilisateur', 'Date', 'Total', 'Statut']]
        for order in orders:
            data.append([
                order.id,
                order.user.username if order.user else '',
                order.created_at.strftime('%d/%m/%Y'),
                f"{order.total:.2f}",
                order.status
            ])
        for row in data:
            yield ','.join(str(cell) for cell in row) + '\n'
    return Response(generate(), mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=commandes.csv"})

@admin_bp.route('/orders', methods=['GET'])
@login_required
@admin_required
def orders():
    from models.order import Order
    search = request.args.get('search','')
    q = Order.query
    if search:
        q = q.join(User, isouter=True).filter(
            (User.username.ilike(f'%{search}%')) | (Order.status.ilike(f'%{search}%'))
        )
    orders = q.all()
    return render_template('pages/admin/orders.html', orders=orders, search=search)

@admin_bp.route('/orders/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_order():
    from models.order import Order
    users = User.query.all()
    if request.method == 'POST':
        user_id = request.form['user_id']
        total = request.form['total']
        status = request.form['status']
        order = Order(user_id=user_id, total=total, status=status)
        db.session.add(order)
        db.session.commit()
        flash('Commande créée avec succès.')
        return redirect(url_for('admin.orders'))
    return render_template('pages/admin/order_form.html', order=None, users=users)

@admin_bp.route('/orders/edit/<int:order_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_order(order_id):
    from models.order import Order
    order = Order.query.get_or_404(order_id)
    users = User.query.all()
    if request.method == 'POST':
        order.user_id = request.form['user_id']
        order.total = request.form['total']
        order.status = request.form['status']
        db.session.commit()
        flash('Commande mise à jour.')
        return redirect(url_for('admin.orders'))
    return render_template('pages/admin/order_form.html', order=order, users=users)

@admin_bp.route('/orders/delete/<int:order_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_order(order_id):
    from models.order import Order
    order = Order.query.get_or_404(order_id)
    if request.method == 'POST':
        db.session.delete(order)
        db.session.commit()
        flash('Commande supprimée.')
        return redirect(url_for('admin.orders'))
    return render_template('pages/admin/order_delete.html', order=order)

@admin_bp.route('/promotions/export')
@login_required
@admin_required
def export_promotions():
    from models.promotion import Promotion
    import csv
    from flask import Response
    promotions = Promotion.query.all()
    def generate():
        data = [['ID', 'Titre', 'Description', 'Réduction', 'Début', 'Fin']]
        for promo in promotions:
            data.append([
                promo.id,
                promo.title,
                promo.description or '',
                promo.discount,
                promo.start_date.strftime('%d/%m/%Y') if promo.start_date else '',
                promo.end_date.strftime('%d/%m/%Y') if promo.end_date else ''
            ])
        for row in data:
            yield ','.join(str(cell) for cell in row) + '\n'
    return Response(generate(), mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=promotions.csv"})

@admin_bp.route('/promotions', methods=['GET'])
@login_required
@admin_required
def promotions():
    from models.promotion import Promotion
    search = request.args.get('search','')
    q = Promotion.query
    if search:
        q = q.filter((Promotion.title.ilike(f'%{search}%')) | (Promotion.description.ilike(f'%{search}%')))
    promotions = q.all()
    return render_template('pages/admin/promotions.html', promotions=promotions, search=search)

@admin_bp.route('/promotions/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_promotion():
    from models.promotion import Promotion
    from datetime import datetime
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        discount = request.form['discount']
        start_date = request.form['start_date'] or None
        end_date = request.form['end_date'] or None
        promo = Promotion(
            title=title,
            description=description,
            discount=discount,
            start_date=datetime.strptime(start_date, '%Y-%m-%d') if start_date else None,
            end_date=datetime.strptime(end_date, '%Y-%m-%d') if end_date else None
        )
        db.session.add(promo)
        db.session.commit()
        flash('Promotion créée avec succès.')
        return redirect(url_for('admin.promotions'))
    return render_template('pages/admin/promotion_form.html', promotion=None)

@admin_bp.route('/promotions/edit/<int:promotion_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_promotion(promotion_id):
    from models.promotion import Promotion
    from datetime import datetime
    promo = Promotion.query.get_or_404(promotion_id)
    if request.method == 'POST':
        promo.title = request.form['title']
        promo.description = request.form['description']
        promo.discount = request.form['discount']
        start_date = request.form['start_date'] or None
        end_date = request.form['end_date'] or None
        promo.start_date = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
        promo.end_date = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None
        db.session.commit()
        flash('Promotion mise à jour.')
        return redirect(url_for('admin.promotions'))
    return render_template('pages/admin/promotion_form.html', promotion=promo)

@admin_bp.route('/promotions/delete/<int:promotion_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_promotion(promotion_id):
    from models.promotion import Promotion
    promo = Promotion.query.get_or_404(promotion_id)
    if request.method == 'POST':
        db.session.delete(promo)
        db.session.commit()
        flash('Promotion supprimée.')
        return redirect(url_for('admin.promotions'))
    return render_template('pages/admin/promotion_delete.html', promotion=promo)
