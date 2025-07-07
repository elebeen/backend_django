from django.test import TestCase
from productos.models import Categoria, Producto, Reseña
from productos.serializers import CategoriaSerializer, ProductoSerializer, ReseñaSerializer
from decimal import Decimal


class SerializerTests(TestCase):

    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Tortas")
        self.producto = Producto.objects.create(
            nombre="Torta Chocolate",
            descripcion="Rica torta",
            precio=Decimal("2.50"),
            categoria=self.categoria
        )

    # 🧪 Prueba 1: Serializa correctamente la categoría
    def test_categoria_serializer(self):
        serializer = CategoriaSerializer(instance=self.categoria)
        self.assertEqual(serializer.data['nombre'], "Tortas")

    # 🧪 Prueba 2: Serializa el producto sin reseñas
    def test_producto_serializer_basico(self):
        serializer = ProductoSerializer(instance=self.producto)
        self.assertEqual(serializer.data['nombre'], "Torta Chocolate")
        self.assertEqual(serializer.data['resenas'], [])

    # 🧪 Prueba 3: Reseña válida se acepta
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

    # 🧪 Prueba 4: Calificación fuera del rango es rechazada
    def test_resena_serializer_calificacion_invalida(self):
        data = {
            "producto": self.producto.id,
            "nombre": "Pedro",
            "comentario": "No tan buena",
            "calificacion": 10
        }
        serializer = ReseñaSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("calificacion", serializer.errors)

    # 🧪 Prueba 5: Producto serializado con reseña incluida
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

    # 🧪 Prueba 6: Nombre vacío en reseña es inválido
    def test_resena_serializer_nombre_vacio(self):
        data = {
            "producto": self.producto.id,
            "nombre": "",
            "comentario": "Comentario válido",
            "calificacion": 3
        }
        serializer = ReseñaSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("nombre", serializer.errors)

    # 🧪 Prueba 7: Comentario vacío en reseña es inválido
    def test_resena_serializer_comentario_vacio(self):
        data = {
            "producto": self.producto.id,
            "nombre": "Carlos",
            "comentario": "",
            "calificacion": 4
        }
        serializer = ReseñaSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("comentario", serializer.errors)

    # 🧪 Prueba 8: Serialización completa de producto con reseña
    def test_producto_serializer_datos_completos(self):
        Reseña.objects.create(
            producto=self.producto,
            nombre="Mario",
            comentario="Buenísimo",
            calificacion=5
        )
        serializer = ProductoSerializer(instance=self.producto)
        self.assertEqual(serializer.data["nombre"], "Torta Chocolate")
        self.assertEqual(serializer.data["categoria"], self.categoria.id)
        self.assertEqual(len(serializer.data["resenas"]), 1)
        self.assertEqual(serializer.data["resenas"][0]["nombre"], "Mario")