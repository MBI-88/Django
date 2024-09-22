from django.contrib import admin
from .models import Libro,Editor,Autor

# Register your models here.

admin.site.site_header = "Control Panel"
admin.site.index_title = "Control Panel Site"
admin.site.site_title = "@MBI"
#admin.site.index_template = ""


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ["titulo","editor","fecha_publicacion"]
    list_filter = ["fecha_publicacion"]
    date_hierarchy = "fecha_publicacion"
    ordering = ["-fecha_publicacion"]
    filter_horizontal = ["autores"]
    raw_id_fields = ["editor"]
    fields = ["titulo","autores","editor","portada"]


@admin.register(Editor)
class EditorAdmin(admin.ModelAdmin):
    pass

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ["nombre","apellidos","email"]
    search_fields = ["nombre","apellidos"]


