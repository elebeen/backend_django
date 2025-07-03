from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    disponible = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre

class Reseña(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='resenas')
    nombre = models.CharField(max_length=100)
    comentario = models.TextField()
    calificacion = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nombre} - {self.calificacion}★'
