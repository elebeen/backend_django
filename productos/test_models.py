from django.test import TestCase
from .models import Categoria, Producto, Reseña
from decimal import Decimal
from django.core.exceptions import ValidationError 

# 🔹 Pruebas para el modelo Categoria
class CategoriaModelTest(TestCase):
    
    def test_str_categoria(self):
        categoria = Categoria.objects.create(nombre="Tortas")
        self.assertEqual(str(categoria), "Tortas")

    # ❗ Nueva: No permitir categoría con nombre vacío
    def test_categoria_nombre_vacio(self):
        categoria = Categoria(nombre="")
        with self.assertRaises(ValidationError):
            categoria.full_clean()


# 🔹 Pruebas para el modelo Producto
class ProductoModelTest(TestCase):
    
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Tortas")

    def test_str_producto(self):
        producto = Producto.objects.create(
            nombre="Torta de Chocolate",
            descripcion="Te llena rapido",
            precio=Decimal("2.50"),
            categoria=self.categoria
        )
        self.assertEqual(str(producto), "Torta de Chocolate")

    def test_precio_producto(self):
        producto = Producto.objects.create(
            nombre="Torta de Chocolate",
            descripcion="Te llena rapido",
            precio=Decimal("2.50"),
            categoria=self.categoria
        )
        self.assertEqual(producto.precio, Decimal("2.50"))

    def test_valor_por_defecto_disponible(self):
        producto = Producto.objects.create(
            nombre="Torta de Chocolate",
            descripcion="Te llena rapido",
            precio=Decimal("2.50"),
            categoria=self.categoria
        )
        self.assertTrue(producto.disponible)

    def test_valor_por_defecto_stock(self):
        producto = Producto.objects.create(
            nombre="Torta de Chocolate",
            descripcion="Te llena rapido",
            precio=Decimal("2.50"),
            categoria=self.categoria
        )
        self.assertEqual(producto.stock, 0)

    def test_relacion_producto_categoria(self):
        producto = Producto.objects.create(
            nombre="Torta de Chocolate",
            descripcion="Torta de Chocolate",
            precio=Decimal("2.50"),
            categoria=self.categoria
        )
        self.assertEqual(producto.categoria.nombre, "Tortas")

    # ❗ Nueva: Producto sin nombre
    def test_producto_sin_nombre(self):
        producto = Producto(
            nombre="",
            descripcion="Sin nombre",
            precio=Decimal("5.00"),
            categoria=self.categoria
        )
        with self.assertRaises(ValidationError):
            producto.full_clean()

    # ❗ Nueva: Producto sin precio
    def test_producto_sin_precio(self):
        producto = Producto(
            nombre="Sin Precio",
            descripcion="No tiene precio",
            categoria=self.categoria
        )
        with self.assertRaises(ValidationError):
            producto.full_clean()

    # ❗ Nueva: Producto con precio negativo
    def test_producto_con_precio_negativo(self):
        producto = Producto(
            nombre="Precio Negativo",
            descripcion="Error",
            precio=Decimal("-10.00"),
            categoria=self.categoria
        )
        with self.assertRaises(ValidationError):
            producto.full_clean()


# 🔹 Pruebas para el modelo Reseña
class ReseñaModelTest(TestCase):
    
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Frappe")
        self.producto = Producto.objects.create(
            nombre="Frappe de Moca",
            descripcion="Rico",
            precio=Decimal("10.50"),
            categoria=self.categoria
        )

    def test_str_resena(self):
        resena = Reseña.objects.create(
            producto=self.producto,
            nombre="Luis",
            comentario="Muy bueno",
            calificacion=4
        )
        self.assertEqual(str(resena), "Luis - 4★")

    def test_creacion_resena_valida(self):
        resena = Reseña.objects.create(
            producto=self.producto,
            nombre="Ana",
            comentario="Excelente calidad",
            calificacion=5
        )
        self.assertEqual(resena.calificacion, 5)

    def test_relacion_resena_producto(self):
        resena = Reseña.objects.create(
            producto=self.producto,
            nombre="Mario",
            comentario="Le falta sabor",
            calificacion=3
        )
        self.assertEqual(resena.producto.nombre, "Frappe de Moca")

    def test_calificacion_fuera_de_rango(self):
        reseña = Reseña(
            producto=self.producto,
            nombre="Error",
            comentario="Calificación inválida",
            calificacion=6
        )
        with self.assertRaises(ValidationError):
            reseña.full_clean()

    # ❗ Nueva: Calificación menor a 1
    def test_calificacion_menor_a_uno(self):
        reseña = Reseña(
            producto=self.producto,
            nombre="Error",
            comentario="Demasiado baja",
            calificacion=0
        )
        with self.assertRaises(ValidationError):
            reseña.full_clean()

    # ❗ Nueva: Reseña sin nombre
    def test_resena_sin_nombre(self):
        reseña = Reseña(
            producto=self.producto,
            nombre="",
            comentario="Sin nombre",
            calificacion=3
        )
        with self.assertRaises(ValidationError):
            reseña.full_clean()

    # ❗ Nueva: Reseña sin comentario
    def test_resena_sin_comentario(self):
        reseña = Reseña(
            producto=self.producto,
            nombre="Luis",
            comentario="",
            calificacion=3
        )
        with self.assertRaises(ValidationError):
            reseña.full_clean()
