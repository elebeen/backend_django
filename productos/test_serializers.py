from django.test import TestCase
from productos.models import Categoria, Producto, Reseña
from productos.serializers import CategoriaSerializer, ProductoSerializer, ReseñaSerializer
from decimal import Decimal


# Clase que agrupa todas las pruebas relacionadas con los serializadores
class SerializerTests(TestCase):

    # Crea una categoría y un producto de prueba reutilizable en todos los test
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Tortas")
        self.producto = Producto.objects.create(
            nombre="Torta Chocolate",
            descripcion="Rica torta",
            precio=Decimal("2.50"),
            categoria=self.categoria
        )

    # 🧪 Prueba 1: Verifica que el serializador de Categoria devuelva correctamente el nombre
    def test_categoria_serializer(self):
        serializer = CategoriaSerializer(instance=self.categoria)
        self.assertEqual(serializer.data['nombre'], "Tortas")

    # 🧪 Prueba 2: Verifica que el producto se serialice correctamente y aún no tenga reseñas
    def test_producto_serializer_basico(self):
        serializer = ProductoSerializer(instance=self.producto)
        self.assertEqual(serializer.data['nombre'], "Torta Chocolate")
        self.assertEqual(serializer.data['resenas'], [])  # El producto aún no tiene reseñas

    # 🧪 Prueba 3: Valida que el serializer acepte una reseña válida
    def test_resena_serializer_valido(self):
        data = {
            "producto": self.producto.id,
            "nombre": "Juan",
            "comentario": "Muy buena",
            "calificacion": 5  # calificación válida
        }
        serializer = ReseñaSerializer(data=data)
        self.assertTrue(serializer.is_valid())  # El serializer debe ser válido
        self.assertEqual(serializer.validated_data['calificacion'], 5)  # Se debe validar correctamente

    # 🧪 Prueba 4: Verifica que el serializer rechace una calificación fuera del rango permitido (1-5)
    def test_resena_serializer_calificacion_invalida(self):
        data = {
            "producto": self.producto.id,
            "nombre": "Pedro",
            "comentario": "No tan buena",
            "calificacion": 10  # calificación inválida
        }
        serializer = ReseñaSerializer(data=data)
        self.assertFalse(serializer.is_valid())  # El serializer debe detectar el error
        self.assertIn("calificacion", serializer.errors)  # El error debe estar en el campo 'calificacion'

    # 🧪 Prueba 5: Verifica que al crear una reseña, el producto serializado incluya esa reseña
    def test_producto_serializer_con_resenas(self):
        # Crea una reseña real en la base de datos de pruebas
        Reseña.objects.create(
            producto=self.producto,
            nombre="Lucía",
            comentario="Recomendado",
            calificacion=4
        )

        # Vuelve a serializar el producto (ahora con una reseña asociada)
        serializer = ProductoSerializer(instance=self.producto)

        # Verifica que el campo 'resenas' contenga una reseña
        self.assertEqual(len(serializer.data['resenas']), 1)

        # Verifica que el nombre de la reseña incluida sea el correcto
        self.assertEqual(serializer.data['resenas'][0]['nombre'], "Lucía")
