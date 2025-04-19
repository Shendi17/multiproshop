from flask import session

class Cart:
    def __init__(self):
        if 'cart' not in session:
            session['cart'] = {}

    def add_item(self, product_id, quantity=1):
        cart = session['cart']
        if str(product_id) in cart:
            cart[str(product_id)] += quantity
        else:
            cart[str(product_id)] = quantity
        session['cart'] = cart
        session.modified = True

    def update_quantity(self, product_id, quantity):
        cart = session['cart']
        if str(product_id) in cart:
            cart[str(product_id)] = quantity
            session['cart'] = cart
            session.modified = True

    def remove_item(self, product_id):
        cart = session['cart']
        if str(product_id) in cart:
            del cart[str(product_id)]
            session['cart'] = cart
            session.modified = True

    def get_items(self):
        return session.get('cart', {})

    def clear(self):
        session['cart'] = {}
        session.modified = True

    def get_total_items(self):
        return sum(session.get('cart', {}).values())
