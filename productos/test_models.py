from django.test import TestCase
from .models import Categoria, Producto, Reseña
from decimal import Decimal
from django.core.exceptions import ValidationError 
# 🔹 Pruebas para el modelo Categoria
class CategoriaModelTest(TestCase):
    
    # Prueba que el método __str__ de Categoria devuelve el nombre correctamente
    def test_str_categoria(self):
        categoria = Categoria.objects.create(nombre="Tortas")
        self.assertEqual(str(categoria), "Tortas")


# 🔹 Pruebas para el modelo Producto
class ProductoModelTest(TestCase):
    
    # Método que se ejecuta antes de cada prueba; crea una categoría base
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Tortas")

    # Prueba que el método __str__ de Producto devuelve su nombre correctamente
    def test_str_producto(self):
        producto = Producto.objects.create(
            nombre="Torta de Chocolate",
            descripcion="Te llena rapido",
            precio=Decimal("2.50"),
            categoria=self.categoria
        )
        self.assertEqual(str(producto), "Torta de Chocolate")

    # Prueba que el precio del producto se guarda correctamente como Decimal
    def test_precio_producto(self):
        producto = Producto.objects.create(
            nombre="Torta de Chocolate",
            descripcion="Te llena rapido",
            precio=Decimal("2.50"),
            categoria=self.categoria
        )
        self.assertEqual(producto.precio, Decimal("2.50"))

    # Prueba que el campo 'disponible' tiene como valor por defecto True
    def test_valor_por_defecto_disponible(self):
        producto = Producto.objects.create(
            nombre="Torta de Chocolate",
            descripcion="Te llena rapido",
            precio=Decimal("2.50"),
            categoria=self.categoria
        )
        self.assertTrue(producto.disponible)

    # Prueba que el campo 'stock' tiene como valor por defecto 0
    def test_valor_por_defecto_stock(self):
        producto = Producto.objects.create(
            nombre="Torta de Chocolate",
            descripcion="Te llena rapido",
            precio=Decimal("2.50"),
            categoria=self.categoria
        )
        self.assertEqual(producto.stock, 0)

    # Prueba que el producto está correctamente relacionado con su categoría
    def test_relacion_producto_categoria(self):
        producto = Producto.objects.create(
            nombre="Torta de Chocolate",
            descripcion="Torta de Chocolate",
            precio=Decimal("2.50"),
            categoria=self.categoria
        )
        self.assertEqual(producto.categoria.nombre, "Tortas")


# 🔹 Pruebas para el modelo Reseña
class ReseñaModelTest(TestCase):
    
    # Prepara una categoría y producto antes de cada prueba
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Frappe")
        self.producto = Producto.objects.create(
            nombre="Frappe de Moca",
            descripcion="Rico",
            precio=Decimal("10.50"),
            categoria=self.categoria
        )

    # Prueba que el método __str__ de Reseña devuelve el formato "nombre - calificación★"
    def test_str_resena(self):
        resena = Reseña.objects.create(
            producto=self.producto,
            nombre="Luis",
            comentario="Muy bueno",
            calificacion=4
        )
        self.assertEqual(str(resena), "Luis - 4★")

    # Prueba que se puede crear una reseña con calificación válida (entre 1 y 5)
    def test_creacion_resena_valida(self):
        resena = Reseña.objects.create(
            producto=self.producto,
            nombre="Ana",
            comentario="Excelente calidad",
            calificacion=5
        )
        self.assertEqual(resena.calificacion, 5)

    # Prueba que la reseña está correctamente relacionada con el producto
    def test_relacion_resena_producto(self):
        resena = Reseña.objects.create(
            producto=self.producto,
            nombre="Mario",
            comentario="Le falta sabor",
            calificacion=3
        )
        self.assertEqual(resena.producto.nombre, "Frappe de Moca")

    # Prueba que al intentar crear una reseña con calificación fuera del rango permitido (1-5), lanza un error
    def test_calificacion_fuera_de_rango(self):
        reseña = Reseña(
            producto=self.producto,
            nombre="Error",
            comentario="Calificación inválida",
            calificacion=6  # fuera del rango 1-5
        )
        with self.assertRaises(ValidationError):
            reseña.full_clean()  # Aquí sí se valida el campo 'choices'





