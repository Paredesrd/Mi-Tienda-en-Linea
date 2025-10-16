from django.contrib import admin
from .models import Category, Brand, Color, FilterPrice, Product, Images, Tag, Contact, Order, OrderItem

class ImagesInline(admin.TabularInline):
    model = Images

class TagInline(admin.TabularInline):
    model = Tag

class ProductAdmin(admin.ModelAdmin):
    inlines = [ImagesInline, TagInline]

# --- CONFIGURACIÓN PARA PEDIDOS ACTUALIZADA ---
class OrderItemInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    # MODIFICACIÓN: Define las columnas que se mostrarán en la lista de pedidos
    list_display = ['user', 'first_name', 'last_name', 'phone', 'email', 'amount', 'paid', 'date']
    # MODIFICACIÓN: Añade una barra de búsqueda
    search_fields = ['first_name', 'last_name', 'email', 'payment_id']
# ----------------------------------------

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(FilterPrice)
admin.site.register(Product, ProductAdmin)
admin.site.register(Contact)

# --- REGISTRO DE NUEVOS MODELOS ---
admin.site.register(Order, OrderAdmin)
# ------------------------------------