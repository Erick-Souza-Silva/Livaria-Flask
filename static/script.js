
// Classe para gerenciar o carrinho de compras
class CartManager {
    constructor() {
        // Inicializa o carrinho vazio ou recupera do localStorage
        this.cart = JSON.parse(localStorage.getItem('cart')) || [];
        this.updateCartCount(); // Atualiza o contador do carrinho na navbar
    }

    // Adiciona um produto ao carrinho
    addToCart(product) {
        // Verifica se o produto já existe no carrinho
        const existingItem = this.cart.find(item => item.id === product.id);
        
        if (existingItem) {
            // Se existe, aumenta a quantidade
            existingItem.quantity += 1;
        } else {
            // Se não existe, adiciona com quantidade 1
            this.cart.push({
                ...product,
                quantity: 1
            });
        }
        
        // Salva no localStorage e atualiza contador
        this.saveCart();
        this.updateCartCount();
        this.showNotification('Produto adicionado ao carrinho!', 'success');
    }

    // Remove um produto do carrinho
    removeFromCart(productId) {
        this.cart = this.cart.filter(item => item.id !== productId);
        this.saveCart();
        this.updateCartCount();
        this.showNotification('Produto removido do carrinho!', 'info');
    }

    // Atualiza a quantidade de um produto
    updateQuantity(productId, newQuantity) {
        const item = this.cart.find(item => item.id === productId);
        if (item) {
            if (newQuantity > 0) {
                item.quantity = newQuantity;
            } else {
                // Se quantidade for 0 ou menor, remove o item
                this.removeFromCart(productId);
                return;
            }
        }
        this.saveCart();
        this.updateCartCount();
    }

    // Calcula o total do carrinho
    getTotal() {
        return this.cart.reduce((total, item) => {
            return total + (item.price * item.quantity);
        }, 0);
    }

    // Obtém a quantidade total de itens
    getTotalItems() {
        return this.cart.reduce((total, item) => total + item.quantity, 0);
    }

    // Limpa o carrinho
    clearCart() {
        this.cart = [];
        this.saveCart();
        this.updateCartCount();
        this.showNotification('Carrinho limpo!', 'info');
    }

    // Salva o carrinho no localStorage
    saveCart() {
        localStorage.setItem('cart', JSON.stringify(this.cart));
    }

    // Atualiza o contador de itens na navbar
    updateCartCount() {
        const cartCountElement = document.getElementById('cart-count');
        if (cartCountElement) {
            cartCountElement.textContent = this.getTotalItems();
        }
    }

    // Exibe notificações para o usuário
    showNotification(message, type = 'info') {
        // Cria elemento de notificação
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; max-width: 300px;';
        
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        // Adiciona ao DOM
        document.body.appendChild(notification);
        
        // Remove automaticamente após 3 segundos
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 3000);
    }
}

// Instância global do gerenciador de carrinho
const cartManager = new CartManager();

// Funções para adicionar produtos ao carrinho
function addToCart(productData) {
    cartManager.addToCart(productData);
}

// Função para formatar preço em Real brasileiro
function formatPrice(price) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(price);
}

// Inicialização quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    // Adiciona evento de clique para todos os botões "Adicionar ao Carrinho"
    const addToCartButtons = document.querySelectorAll('.btn-add-to-cart');
    
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault(); // Previne comportamento padrão do link
            
            // Obtém dados do produto do botão
            const productData = {
                id: this.dataset.productId,
                name: this.dataset.productName,
                price: parseFloat(this.dataset.productPrice),
                image: this.dataset.productImage || 'https://via.placeholder.com/150'
            };
            
            addToCart(productData);
        });
    });

    // Funcionalidade de busca
    const searchForm = document.querySelector('form.d-flex');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const searchTerm = this.querySelector('input[type="search"]').value.trim();
            
            if (searchTerm) {
                // Simula busca (em um projeto real, faria requisição ao servidor)
                cartManager.showNotification(`Buscando por: "${searchTerm}"`, 'info');
                // Aqui você redirecionaria para uma página de resultados
                // window.location.href = `busca.html?q=${encodeURIComponent(searchTerm)}`;
            }
        });
    }

    // Smooth scroll para links âncora
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Animação de fade-in para elementos quando entram na viewport
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);

    // Observa todos os cards para animação
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        observer.observe(card);
    });

    // Funcionalidade para validação de formulários
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
});

// Função para simular processo de checkout
function processCheckout() {
    if (cartManager.cart.length === 0) {
        cartManager.showNotification('Carrinho vazio!', 'warning');
        return;
    }

    // Simula processamento do pedido
    cartManager.showNotification('Processando pedido...', 'info');
    
    setTimeout(() => {
        cartManager.clearCart();
        cartManager.showNotification('Pedido realizado com sucesso!', 'success');
        // Em um projeto real, redirecionaria para página de confirmação
        // window.location.href = 'confirmacao.html';
    }, 2000);
}

// Função para toggle do menu mobile (caso necessário)
function toggleMobileMenu() {
    const navbarCollapse = document.querySelector('.navbar-collapse');
    if (navbarCollapse) {
        navbarCollapse.classList.toggle('show');
    }
}

// Função para lazy loading de imagens (otimização)
function setupLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));
}

// Função para voltar ao topo da página
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Adiciona botão "Voltar ao Topo" quando necessário
window.addEventListener('scroll', function() {
    const scrollButton = document.getElementById('scroll-to-top');
    if (scrollButton) {
        if (window.pageYOffset > 300) {
            scrollButton.style.display = 'block';
        } else {
            scrollButton.style.display = 'none';
        }
    }
});
