from django.contrib import admin
from .models import *

@admin.register(TipoConvocatoria)
class TipoConvocatoriaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre']
    search_fields = ['nombre']

@admin.register(Aprendiz)
class AprendizAdmin(admin.ModelAdmin):
    list_display = ['identificacion', 'usuario', 'ficha', 'programa', 'fecha_registro']
    search_fields = ['identificacion', 'usuario__first_name', 'usuario__last_name']
    list_filter = ['programa', 'ficha']

@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'cargo']
    search_fields = ['usuario__first_name', 'usuario__last_name', 'cargo']

@admin.register(Convocatoria)
class ConvocatoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo', 'fecha_inicio', 'fecha_final', 'cantidad_beneficiarios', 'activa']
    list_filter = ['tipo', 'activa', 'fecha_inicio']
    search_fields = ['nombre']
    date_hierarchy = 'fecha_inicio'

@admin.register(Postulacion)
class PostulacionAdmin(admin.ModelAdmin):
    list_display = ['aprendiz', 'convocatoria', 'fecha_postulacion', 'estado', 'puntaje']
    list_filter = ['estado', 'convocatoria__tipo', 'fecha_postulacion']
    search_fields = ['aprendiz__usuario__first_name', 'aprendiz__usuario__last_name', 'convocatoria__nombre']

@admin.register(Evaluacion)
class EvaluacionAdmin(admin.ModelAdmin):
    list_display = ['postulacion', 'funcionario', 'puntaje', 'fecha_evaluacion']
    list_filter = ['funcionario', 'fecha_evaluacion']
    search_fields = ['postulacion__aprendiz__usuario__first_name', 'funcionario__usuario__first_name']