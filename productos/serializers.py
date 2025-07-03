from rest_framework import serializers
from .models import Categoria, Producto, Reseña

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ReseñaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reseña
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    resenas = ReseñaSerializer(many=True, read_only=True)  # 👈 relaciones

    class Meta:
        model = Producto
        fields = '__all__'
