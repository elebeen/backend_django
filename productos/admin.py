from django.contrib import admin
from .models import Categoria, Producto, Reseña  # 👈 añadimos Reseña

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio', 'stock', 'disponible']
    list_filter = ['categoria', 'disponible']
    search_fields = ['nombre']

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre']

@admin.register(Reseña)
class ReseñaAdmin(admin.ModelAdmin):
    list_display = ['producto', 'nombre', 'calificacion', 'creado_en']
    list_filter = ['calificacion', 'producto']
    search_fields = ['nombre', 'comentario']

