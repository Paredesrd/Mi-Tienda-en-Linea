from django.urls import path
from . import views

urlpatterns = [
    # URL para la página principal
    path('', views.index, name='index'),

    # URL para la página de la tienda
    path('shop/', views.shop, name='shop'),

    # URL para la página de resultados de búsqueda
    path('search/', views.search, name='search'),

    # URL para la página de detalles de un producto
    path('product/<int:pk>/', views.product_detail, name='product_detail'),

    # URL para la página de contacto
    path('contact/', views.contact_page, name='contact'),

    # URLs de Autenticación
    path('register/', views.handle_register, name='register'),
    path('login/', views.handle_login, name='login'),
    path('logout/', views.handle_logout, name='logout'),

    # URLs del Carrito
    path('cart/', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart_delete/<str:product_id>/', views.cart_delete, name='cart_delete'),

    # URLs de Pago
    path('checkout/', views.checkout, name='checkout'),
    path('place_order/<int:order_id>/', views.place_order, name='place_order'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('success/', views.success, name='success'),

    # --- NUEVA URL DE "MIS PEDIDOS" AÑADIDA ---
    path('your-orders/', views.your_order, name='your_order'),
]