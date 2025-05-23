from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_required, current_user
from models.product import Product
from models.order import Order, OrderItem
from extensions import db

cart = Blueprint('cart', __name__)

@cart.route('/add', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id', type=int)
    quantity = request.form.get('quantity', 1, type=int)
    
    if not product_id:
        flash('Produit invalide', 'error')
        return redirect(url_for('products.list_products'))
    
    product = Product.query.get_or_404(product_id)
    
    if product.stock < quantity:
        flash('Stock insuffisant', 'error')
        return redirect(url_for('products.product_detail', product_id=product_id))
    
    cart = session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
    session['cart'] = cart
    
    flash(f'{quantity} {product.name} ajouté(s) au panier', 'success')
    return redirect(url_for('products.product_detail', product_id=product_id))

@cart.route('/')
def view_cart():
    cart = session.get('cart', {})
    cart_items = []
    total = 0
    
    for product_id, quantity in cart.items():
        product = Product.query.get(int(product_id))
        if product:
            subtotal = product.price * quantity
            total += subtotal
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
    
    return render_template('pages/cart.html',
                         cart_items=cart_items,
                         total=total)

@cart.route('/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        session['cart'] = cart
        flash('Produit retiré du panier', 'success')
    return redirect(url_for('cart.view_cart'))

@cart.route('/update/<int:product_id>', methods=['POST'])
def update_quantity(product_id):
    cart = session.get('cart', {})
    action = request.form.get('action')
    
    if str(product_id) in cart:
        current_quantity = cart[str(product_id)]
        if action == 'increase':
            product = Product.query.get(product_id)
            if product and product.stock > current_quantity:
                cart[str(product_id)] = current_quantity + 1
        elif action == 'decrease' and current_quantity > 1:
            cart[str(product_id)] = current_quantity - 1
        
        session['cart'] = cart
    
    return redirect(url_for('cart.view_cart'))

@cart.route('/cart-total-items')
def cart_total_items():
    cart = session.get('cart', {})
    total = sum(cart.values())
    return jsonify({'total': total})

@cart.route('/add-item', methods=['POST'])
def add_item():
    data = request.get_json()
    product_id = data.get('product_id', type=int)
    quantity = data.get('quantity', 1)
    if not product_id:
        return jsonify({'success': False, 'message': 'Produit invalide.'}), 400
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'success': False, 'message': 'Produit introuvable.'}), 404
    if product.stock < quantity:
        return jsonify({'success': False, 'message': 'Stock insuffisant.'}), 400
    cart = session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
    session['cart'] = cart
    session.modified = True
    total = sum(cart.values())
    return jsonify({'success': True, 'message': f'{quantity} {product.name} ajouté(s) au panier.', 'cart_total': total})

@cart.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    if request.method == 'POST':
        cart = session.get('cart', {})
        if not cart:
            flash('Votre panier est vide', 'error')
            return redirect(url_for('cart.view_cart'))
        
        total = 0
        order_items = []
        
        for product_id, quantity in cart.items():
            product = Product.query.get(int(product_id))
            if product and product.stock >= quantity:
                subtotal = product.price * quantity
                total += subtotal
                
                # Mettre à jour le stock
                product.stock -= quantity
                
                # Créer l'item de commande
                order_item = OrderItem(
                    product_id=product.id,
                    quantity=quantity,
                    price=product.price
                )
                order_items.append(order_item)
            else:
                flash(f'Stock insuffisant pour {product.name}', 'error')
                return redirect(url_for('cart.view_cart'))
        
        # Créer la commande
        order = Order(
            user_id=current_user.id,
            total_price=total,
            status='En attente'
        )
        
        # Ajouter les items à la commande
        for item in order_items:
            order.order_items.append(item)
        
        try:
            db.session.add(order)
            db.session.commit()
            
            # Vider le panier
            session['cart'] = {}
            
            flash('Commande effectuée avec succès!', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            flash('Une erreur est survenue lors de la commande', 'error')
            return redirect(url_for('cart.view_cart'))
    
    return render_template('pages/checkout.html', cart=session.get('cart', {}))
