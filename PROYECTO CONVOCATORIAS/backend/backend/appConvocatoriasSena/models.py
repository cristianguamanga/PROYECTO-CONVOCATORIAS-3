from django.db import models
from django.contrib.auth.models import User
import requests
import json

class TipoConvocatoria(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

class Aprendiz(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    identificacion = models.CharField(max_length=20, unique=True)
    ficha = models.CharField(max_length=50)
    programa = models.CharField(max_length=200)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.usuario.first_name} {self.usuario.last_name} - {self.identificacion}"
    
    @classmethod
    def verificar_matricula(cls, identificacion):
        """Verifica si el aprendiz está matriculado en el JSON externo"""
        try:
            url = "https://raw.githubusercontent.com/CesarMCuellarCha/apis/refs/heads/main/SENACTPI.matriculados.json"
            response = requests.get(url)
            if response.status_code == 200:
                aprendices = response.json()
                for ap in aprendices:
                    if str(ap.get('identificacion')) == str(identificacion):
                        return {
                            'identificacion': ap.get('identificacion'),
                            'nombres': ap.get('nombres'),
                            'apellidos': ap.get('apellidos'),
                            'ficha': ap.get('ficha'),
                            'programa': ap.get('programa')
                        }
            return None
        except Exception as e:
            print(f"Error consultando API: {e}")
            return None

class Funcionario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    cargo = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.usuario.first_name} {self.usuario.last_name} - {self.cargo}"

class Convocatoria(models.Model):
    nombre = models.CharField(max_length=200)
    tipo = models.ForeignKey(TipoConvocatoria, on_delete=models.CASCADE)
    cantidad_beneficiarios = models.IntegerField()
    fecha_inicio = models.DateTimeField()
    fecha_final = models.DateTimeField()
    documento = models.FileField(upload_to='documentos/')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activa = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre

class Postulacion(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('APROBADO', 'Aprobado'),
        ('RECHAZADO', 'Rechazado'),
    ]
    
    aprendiz = models.ForeignKey(Aprendiz, on_delete=models.CASCADE)
    convocatoria = models.ForeignKey(Convocatoria, on_delete=models.CASCADE)
    fecha_postulacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    puntaje = models.IntegerField(null=True, blank=True)
    
    class Meta:
        unique_together = ['aprendiz', 'convocatoria']
    
    def __str__(self):
        return f"{self.aprendiz} - {self.convocatoria}"

class Evaluacion(models.Model):
    postulacion = models.ForeignKey(Postulacion, on_delete=models.CASCADE)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    puntaje = models.IntegerField()
    observaciones = models.TextField(blank=True)
    fecha_evaluacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Evaluación {self.postulacion} - {self.puntaje}"