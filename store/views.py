from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import Product, Category, Brand, Color, FilterPrice, Contact, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from cart.cart import Cart


# Ya no necesitamos importar razorpay por ahora
# import razorpay

# Vista para la página principal
def index(request):
    products = Product.objects.filter(status='Publish')
    context = {'products': products}
    return render(request, 'main/index.html', context)


# ... (otras vistas sin cambios: shop, search, product_detail, contact_page, register, login, logout, etc.) ...
# (He omitido el código sin cambios para mayor claridad, pero asegúrate de que esté en tu archivo)

# Vista para la página de la tienda
def shop(request):
    # ... (código sin cambios)
    category_id = request.GET.get('category')
    filter_price_id = request.GET.get('filter_price')
    color_id = request.GET.get('color')
    brand_id = request.GET.get('brand')
    sort_by = request.GET.get('sort')
    new_product_param = request.GET.get('new_product')
    old_product_param = request.GET.get('old_product')
    products = Product.objects.filter(status='Publish')
    if category_id:
        products = products.filter(category=category_id)
    if filter_price_id:
        products = products.filter(filter_price=filter_price_id)
    if color_id:
        products = products.filter(color=color_id)
    if brand_id:
        products = products.filter(brand=brand_id)
    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    if new_product_param:
        products = products.filter(condition='New').order_by('-id')
    if old_product_param:
        products = products.filter(condition='Old').order_by('-id')
    categories = Category.objects.all()
    brands = Brand.objects.all()
    colors = Color.objects.all()
    filter_prices = FilterPrice.objects.all()
    context = {
        'products': products,
        'categories': categories,
        'brands': brands,
        'colors': colors,
        'filter_prices': filter_prices,
    }
    return render(request, 'store/shop.html', context)


# Vista de Búsqueda
def search(request):
    query = request.GET.get('query')
    products = Product.objects.filter(name__icontains=query, status='Publish')
    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'store/search.html', context)


# Vista de Detalles del Producto
def product_detail(request, pk):
    product = Product.objects.get(id=pk)
    context = {
        'product': product,
    }
    return render(request, 'store/product_detail.html', context)


# Vista de la Página de Contacto
def contact_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        email_message = f"""
        Nuevo mensaje de contacto de: {name} ({email})
        """
        try:
            send_mail(subject, email_message, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], fail_silently=False)
            contact = Contact(name=name, email=email, subject=subject, message=message)
            contact.save()
            return redirect('index')
        except Exception as e:
            print(e)
            return render(request, 'store/contact.html')
    return render(request, 'store/contact.html')


# Vistas de Autenticación
def handle_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        my_user = User.objects.create_user(username, email, pass1)
        my_user.save()
        return redirect('index')
    return render(request, 'registration/login.html')


def handle_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        passw = request.POST.get('password')
        user = authenticate(username=username, password=passw)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return redirect('login')
    return render(request, 'registration/login.html')


def handle_logout(request):
    logout(request)
    return redirect('index')


# ================= VISTAS DEL CARRITO =================
@login_required(login_url='/login/')
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    cart.add(product=product)
    request.session.modified = True
    next_page = request.GET.get('next', 'cart_detail')
    return redirect(next_page)


@login_required(login_url='/login/')
def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    item_id = str(product.id)  # Las claves de la sesión son strings

    if request.GET.get('delete_all') == 'true':
        cart.remove(product)
    else:
        if item_id in request.session['cart'] and request.session['cart'][item_id]['quantity'] > 1:
            request.session['cart'][item_id]['quantity'] -= 1
        else:
            cart.remove(product)

    request.session.modified = True
    next_page = request.GET.get('next', 'cart_detail')
    return redirect(next_page)


@login_required(login_url='/login/')
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


@login_required(login_url='/login/')
def cart_delete(request, product_id):
    product = Product.objects.get(id=int(product_id))
    cart = Cart(request)
    cart.remove(product)
    request.session.modified = True
    return redirect(request.META.get('HTTP_REFERER', 'shop'))


# --- VISTA DE CHECKOUT ACTUALIZADA ---
@login_required(login_url='/login/')
def checkout(request):
    cart = Cart(request)

    # --- LÓGICA DE PROCESAMIENTO DEL FORMULARIO DE CHECKOUT ---
    # Esto se ejecuta cuando el usuario envía el formulario de facturación
    if request.method == 'POST' and 'first_name' in request.POST:
        cart_total_amount = 0
        if request.session.get('cart'):
            for key, value in request.session['cart'].items():
                cart_total_amount += float(value['price']) * value['quantity']

        new_order = Order.objects.create(
            user=request.user,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            country=request.POST.get('country'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            postcode=request.POST.get('postcode'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email'),
            amount=cart_total_amount,
            payment_id=request.POST.get('payment_id'),
            paid=False
        )

        for key, value in request.session['cart'].items():
            OrderItem.objects.create(
                order=new_order,
                product=value['name'],
                image=value['image'],
                quantity=value['quantity'],
                price=value['price'],
                total=float(value['price']) * value['quantity']
            )

        del request.session['cart']
        request.session.modified = True

        return redirect('place_order', order_id=new_order.id)

    # --- LÓGICA PARA MOSTRAR LA PÁGINA DE CHECKOUT ---
    # Esto se ejecuta cuando el usuario llega a la página de checkout (GET o POST desde el carrito)
    cart_total_amount = 0
    # Priorizamos el monto enviado desde el carrito (POST) como en el video
    if request.method == 'POST' and 'amount' in request.POST:
        cart_total_amount = float(request.POST.get('amount'))
    # Si no, lo calculamos desde la sesión (para acceso directo por GET)
    elif request.session.get('cart'):
        for key, value in request.session['cart'].items():
            cart_total_amount += float(value['price']) * value['quantity']

    # --- SIMULACIÓN DE PASARELA DE PAGO ---
    payment = {'id': 'pago_simulado_12345'}

    context = {
        'cart': cart,
        'cart_total_amount': cart_total_amount,
        'payment': payment
    }
    return render(request, 'store/checkout.html', context)


# --- VISTA DE PLACE ORDER ACTUALIZADA ---
@login_required(login_url='/login/')
def place_order(request, order_id):
    order = Order.objects.get(id=order_id)
    context = {'order': order}
    return render(request, 'store/place_order.html', context)


# --- NUEVA VISTA DE CONFIRMACIÓN DE PAGO ---
@login_required(login_url='/login/')
def payment_success(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)
        order.paid = True
        order.save()
        return redirect('success')
    return redirect('shop')


# --- VISTA DE SUCCESS (Página de Agradecimiento) ---
@login_required(login_url='/login/')
def success(request):
    return render(request, 'store/thank_you.html')


# --- NUEVA VISTA DE "MIS PEDIDOS" ---
@login_required(login_url='/login/')
def your_order(request):
    # Obtenemos el usuario que ha iniciado sesión
    user = request.user
    # Buscamos todos los OrderItem cuyos pedidos ('order') pertenecen a ese usuario
    orders = OrderItem.objects.filter(order__user=user)

    context = {
        'orders': orders,
    }
    return render(request, 'store/your_order.html', context)


# ------------------------------------


# Vista para la plantilla base (la que usamos para probar)
def base(request):
    return render(request, 'main/base.html')