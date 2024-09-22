from django.db import models
from django.urls import reverse

# Create your models here.

class Editor(models.Model):
    nombre = models.CharField(max_length = 30)
    domicilio = models.CharField(max_length = 50)
    ciudad = models.CharField(max_length = 60)
    estado = models.CharField(max_length = 30)
    pais = models.CharField(max_length = 50)
    website = models.URLField()

    class Meta:
        ordering = ['nombre']
        verbose_name_plural = 'Editores'

    def __str__(self) -> str:
        return self.nombre

class Autor(models.Model):
    nombre = models.CharField(max_length = 30)
    apellidos = models.CharField(max_length = 40)
    email = models.EmailField(blank = True,verbose_name = 'e-mail')
    ultimo_acceso = models.DateTimeField(blank = True, null = True)

    def get_absolute_url(self) -> reverse:
        return reverse('detalles-autor', kwargs = {'pk':self.pk})

    class Meta:
        verbose_name_plural = 'Autores'

    def __str__(self) -> str:
        return  "{} {}".format(self.nombre,self.apellidos)

# Extendiendo las funcionalidades de la clase Libro
class ManejadorLibros(models.Manager):
    def contar_titulos(self, keyword:str) -> int:
        return self.filter(titulo = keyword).count()

# Metodo personalizado de busqueda
class BarriosLibrosManager(models.Manager):
    def get_query_set(self) -> list[str]:
        return super(BarriosLibrosManager,self).get_queryset().filter(autor = 'Maikel Barrios Insua')

class Libro(models.Model):
    titulo = models.CharField(max_length = 100)
    autores = models.ManyToManyField(Autor)
    editor = models.ForeignKey(Editor, on_delete = models.CASCADE)
    fecha_publicacion = models.DateField(blank = True, null = True)
    portada = models.ImageField(upload_to = 'portadas')
    num_paginas = models.IntegerField(blank = True,null = True)

    barrios_objects = BarriosLibrosManager()
    objects = ManejadorLibros()

    class Meta:
        ordering = ['fecha_publicacion']
        verbose_name_plural = 'Libros'
    def __str__(self) -> str:
        return self.titulo

class ManagerEncuestas(models.Manager):
    def contar(self) -> list[str]:
        from django.db import connection

        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT x.id, x.pregunta, x.fecha, COUNT (*)
            FROM biblioteca_opinion x, biblioteca_respuestas y
            WHERE x.id = y.encuesta_id
            GROUP BY x.id, x.pregunta, x.fecha
            ORDER BY x.fecha DESC
            """)
        
        lista_resultados = []
        for row in cursor.fetchall():
            p = self.model(id = row[0], pregunta = row[1], fecha = row[2])
            p.num_respuesta = row[3]
            lista_resultados.append(p)
        return lista_resultados

class Opinion(models.Model):
    pregunta = models.CharField(max_length = 200)
    fecha = models.DateField(blank = True, null = True)
    objects = ManagerEncuestas()

class Respuestas(models.Model):
    encuesta = models.ForeignKey(Opinion,on_delete = models.CASCADE)
    nombre = models.CharField(max_length = 50)
    respuesta = models.TextField()

class ManejadorMujeres(models.Manager):
    def get_query_set(self) -> list[str]:
        return super(ManejadorMujeres, self).get_queryset().filter(sexo = 'M')

class ManejadorHombres(models.Manager):
    def get_query_set(self) -> list[str]:
        return super(ManejadorHombres, self).get_queryset().filter(sexo = 'H')

class Persona(models.Model):
    nombre = models.CharField(max_length = 15)
    apellidos = models.CharField(max_length = 30)
    sexo = models.CharField(max_length = 1, choices = (('M','Mujer'), ('H','Hombre')))
    nacimiento = models.DateField(blank = True, null = True)
    domicilio = models.CharField(max_length = 100, null = True)
    ciudad = models.CharField(max_length = 15, null = True)
    estado = models.CharField(max_length = 2, null = True)

    gente = models.Manager()
    hombres = ManejadorHombres()
    mujer = ManejadorMujeres() 

    def estatus_bebe(self) -> str:
        import datetime
        if datetime.date(1945, 8, 1) <= self.nacimiento <= datetime.date(1964, 12, 31):
            return "Baby boomer"
        elif self.nacimiento > datetime.date(1945, 8, 1):
            return "Pre-boomer"
        return "Post-boomer"
    
    def es_del_medio(self) -> str:
        return self.estado in ('IL', "WI", "IN", "OH", "IA", "MO")
    
    def _nobmre_completo(self) -> str:
        return '%s %s' % (self.nombre,self.apellidos)
