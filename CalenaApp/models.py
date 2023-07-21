from django.db import models

# Create your models here.
class Marca(models.Model):
    id_marca = models.AutoField(primary_key=True)
    nombre_marca = models.CharField(max_length=100)
    logo_marca = models.ImageField(upload_to='', blank=True)
    catalogo_pdf = models.FileField(upload_to='', blank=True)

    def __str__(self):
        return self.nombre_marca

class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre_categoria

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    titulo_producto = models.CharField(max_length=200)
    marca_producto = models.ForeignKey(Marca, on_delete=models.CASCADE)
    categoria_producto = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    codigo_producto = models.CharField(max_length=200)
    unidadMedida_producto = models.CharField(max_length=200)
    imagen_producto = models.ImageField(upload_to='', blank=True)

    def __str__(self):
        return self.codigo_producto