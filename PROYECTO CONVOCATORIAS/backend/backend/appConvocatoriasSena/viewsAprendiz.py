from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db import transaction
import json
from .models import *

@csrf_exempt
def registrar_aprendiz(request):
    try:
        if request.method == 'POST':
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                identificacion = data.get('identificacion')
                correo = data.get('correo')
            else:
                identificacion = request.POST.get('identificacion')
                correo = request.POST.get('correo')
            
            if not identificacion or not correo:
                return JsonResponse({"mensaje": "Identificación y correo son obligatorios"}, status=400)
            
            
            datos_aprendiz = Aprendiz.verificar_matricula(identificacion)
            if not datos_aprendiz:
                return JsonResponse({"mensaje": "Aprendiz no encontrado en matriculados 2025"}, status=400)
            
        
            if User.objects.filter(username=correo).exists():
                return JsonResponse({"mensaje": "El correo ya está registrado"}, status=400)
            
            if Aprendiz.objects.filter(identificacion=identificacion).exists():
                return JsonResponse({"mensaje": "El aprendiz ya está registrado"}, status=400)
            
            with transaction.atomic():
            
                usuario = User(
                    username=correo,
                    first_name=datos_aprendiz['nombres'],
                    last_name=datos_aprendiz['apellidos'],
                    email=correo,
                    is_active=True
                )
                usuario.set_password("12345")
                usuario.save()
                
            
                aprendiz = Aprendiz(
                    usuario=usuario,
                    identificacion=identificacion,
                    ficha=datos_aprendiz['ficha'],
                    programa=datos_aprendiz['programa']
                )
                aprendiz.save()
                
                mensaje = "Aprendiz registrado correctamente"
                return JsonResponse({
                    "mensaje": mensaje,
                    "aprendiz": {
                        "id": aprendiz.id,
                        "nombres": datos_aprendiz['nombres'],
                        "apellidos": datos_aprendiz['apellidos'],
                        "identificacion": identificacion,
                        "ficha": datos_aprendiz['ficha'],
                        "programa": datos_aprendiz['programa']
                    }
                })
        else:
            return JsonResponse({"mensaje": "Método no permitido"}, status=405)
    except Exception as e:
        return JsonResponse({"mensaje": f"Error: {str(e)}"}, status=500)

@csrf_exempt
def postularse(request):
    try:
        if request.method == 'POST':
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                aprendiz_id = data.get('aprendiz_id')
                convocatoria_id = data.get('convocatoria_id')
            else:
                aprendiz_id = request.POST.get('aprendiz_id')
                convocatoria_id = request.POST.get('convocatoria_id')
            
            if not aprendiz_id or not convocatoria_id:
                return JsonResponse({"mensaje": "Faltan datos obligatorios"}, status=400)
            
            aprendiz = Aprendiz.objects.get(id=aprendiz_id)
            convocatoria = Convocatoria.objects.get(id=convocatoria_id)
            
            
            if Postulacion.objects.filter(aprendiz=aprendiz, convocatoria=convocatoria).exists():
                return JsonResponse({"mensaje": "Ya estás postulado a esta convocatoria"}, status=400)
            
            
            if not convocatoria.activa:
                return JsonResponse({"mensaje": "La convocatoria no está activa"}, status=400)
            
            postulacion = Postulacion(aprendiz=aprendiz, convocatoria=convocatoria)
            postulacion.save()
            
        
            
            return JsonResponse({
                "mensaje": "Postulación realizada correctamente",
                "postulacion_id": postulacion.id
            })
        else:
            return JsonResponse({"mensaje": "Método no permitido"}, status=405)
    except Aprendiz.DoesNotExist:
        return JsonResponse({"mensaje": "Aprendiz no encontrado"}, status=404)
    except Convocatoria.DoesNotExist:
        return JsonResponse({"mensaje": "Convocatoria no encontrada"}, status=404)
    except Exception as e:
        return JsonResponse({"mensaje": f"Error: {str(e)}"}, status=500)

def mis_postulaciones(request):
    try:
        aprendiz_id = request.GET.get('aprendiz_id')
        if not aprendiz_id:
            return JsonResponse({"mensaje": "Se requiere aprendiz_id"}, status=400)
        
        aprendiz = Aprendiz.objects.get(id=aprendiz_id)
        postulaciones = Postulacion.objects.filter(aprendiz=aprendiz).order_by('-fecha_postulacion')
        
        data = []
        for post in postulaciones:
            data.append({
                'id': post.id,
                'convocatoria': post.convocatoria.nombre,
                'tipo_convocatoria': post.convocatoria.tipo.nombre,
                'fecha_postulacion': post.fecha_postulacion.strftime('%Y-%m-%d %H:%M:%S'),
                'estado': post.estado,
                'puntaje': post.puntaje,
                'convocatoria_activa': post.convocatoria.activa
            })
        
        return JsonResponse(data, safe=False)
    except Aprendiz.DoesNotExist:
        return JsonResponse({"mensaje": "Aprendiz no encontrado"}, status=404)
    except Exception as e:
        return JsonResponse({"mensaje": f"Error: {str(e)}"}, status=500)