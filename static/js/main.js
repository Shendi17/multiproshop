// Fonction pour mettre à jour le compteur du panier
function updateCartCount(count) {
    const cartCount = document.querySelector('.cart-count');
    if (cartCount) {
        if (count > 0) {
            cartCount.textContent = count;
            cartCount.style.display = 'inline';
        } else {
            cartCount.style.display = 'none';
        }
    }
}

// Fonction pour ajouter un produit au panier
function addToCart(productId, quantity = 1) {
    fetch(`/cart/add/${productId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({ quantity: quantity })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Mettre à jour le compteur du panier
            updateCartCount(data.cart_count);
            
            // Afficher un message de succès
            showAlert('success', 'Produit ajouté au panier avec succès !');
        } else {
            showAlert('danger', data.message || 'Une erreur est survenue');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('danger', 'Une erreur est survenue lors de l\'ajout au panier');
    });
}

// Fonction pour mettre à jour la quantité dans le panier
function updateCartQuantity(productId, quantity) {
    if (quantity < 1) return;
    
    fetch(`/cart/update/${productId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({ quantity: quantity })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Mettre à jour le prix total
            const totalElement = document.getElementById('cart-total');
            if (totalElement) {
                totalElement.textContent = data.total.toFixed(2) + ' €';
            }
            
            // Mettre à jour le sous-total du produit
            const subtotalElement = document.getElementById(`subtotal-${productId}`);
            if (subtotalElement) {
                subtotalElement.textContent = data.subtotal.toFixed(2) + ' €';
            }
            
            updateCartCount(data.cart_count);
        } else {
            showAlert('danger', data.message || 'Une erreur est survenue');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('danger', 'Une erreur est survenue lors de la mise à jour du panier');
    });
}

// Fonction pour supprimer un produit du panier
function removeFromCart(productId) {
    fetch(`/cart/remove/${productId}`, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Supprimer la ligne du produit
            const productRow = document.getElementById(`cart-item-${productId}`);
            if (productRow) {
                productRow.remove();
            }
            
            // Mettre à jour le total
            const totalElement = document.getElementById('cart-total');
            if (totalElement) {
                totalElement.textContent = data.total.toFixed(2) + ' €';
            }
            
            updateCartCount(data.cart_count);
            
            // Si le panier est vide, rafraîchir la page
            if (data.cart_count === 0) {
                location.reload();
            }
        } else {
            showAlert('danger', data.message || 'Une erreur est survenue');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('danger', 'Une erreur est survenue lors de la suppression du produit');
    });
}

// Fonction pour afficher les alertes
function showAlert(type, message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    // Supprimer l'alerte après 3 secondes
    setTimeout(() => {
        alertDiv.remove();
    }, 3000);
}

// Gestionnaires d'événements pour les boutons de quantité
document.addEventListener('DOMContentLoaded', function() {
    // Gérer les boutons d'incrémentation/décrémentation de quantité
    document.querySelectorAll('.quantity-input').forEach(input => {
        const productId = input.dataset.productId;
        
        // Bouton moins
        input.previousElementSibling?.addEventListener('click', () => {
            const newValue = parseInt(input.value) - 1;
            if (newValue >= 1) {
                input.value = newValue;
                updateCartQuantity(productId, newValue);
            }
        });
        
        // Bouton plus
        input.nextElementSibling?.addEventListener('click', () => {
            const newValue = parseInt(input.value) + 1;
            input.value = newValue;
            updateCartQuantity(productId, newValue);
        });
        
        // Changement manuel de la valeur
        input.addEventListener('change', () => {
            let newValue = parseInt(input.value);
            if (isNaN(newValue) || newValue < 1) {
                newValue = 1;
                input.value = newValue;
            }
            updateCartQuantity(productId, newValue);
        });
    });
    
    // Initialiser les tooltips Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});
