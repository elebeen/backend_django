
from django.test import TestCase
from productos.models import Categoria, Producto, Reseña
from productos.serializers import CategoriaSerializer, ProductoSerializer, ReseñaSerializer
from decimal import Decimal

class SerializerTests(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Tecnología")
        self.producto = Producto.objects.create(
            nombre="Laptop",
            descripcion="Gaming",
            precio=Decimal("2999.99"),
            categoria=self.categoria
        )

    def test_categoria_serializer(self):
        serializer = CategoriaSerializer(instance=self.categoria)
        self.assertEqual(serializer.data['nombre'], "Tecnología")

    def test_producto_serializer_basico(self):
        serializer = ProductoSerializer(instance=self.producto)
        self.assertEqual(serializer.data['nombre'], "Laptop")
        self.assertEqual(serializer.data['resenas'], [])  # sin reseñas todavía

    def test_resena_serializer_valido(self):
        data = {
            "producto": self.producto.id,
            "nombre": "Juan",
            "comentario": "Muy buena",
            "calificacion": 5
        }
        serializer = ReseñaSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['calificacion'], 5)

    def test_resena_serializer_calificacion_invalida(self):
        data = {
            "producto": self.producto.id,
            "nombre": "Pedro",
            "comentario": "No tan buena",
            "calificacion": 10  # fuera de rango
        }
        serializer = ReseñaSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("calificacion", serializer.errors)

    def test_producto_serializer_con_resenas(self):
        Reseña.objects.create(
            producto=self.producto,
            nombre="Lucía",
            comentario="Recomendado",
            calificacion=4
        )
        serializer = ProductoSerializer(instance=self.producto)
        self.assertEqual(len(serializer.data['resenas']), 1)
        self.assertEqual(serializer.data['resenas'][0]['nombre'], "Lucía")



