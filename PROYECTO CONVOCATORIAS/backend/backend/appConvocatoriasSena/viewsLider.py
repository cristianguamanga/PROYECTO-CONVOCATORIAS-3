from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db import transaction, Error
from datetime import datetime
import json
from .models import *

formato_fecha = '%Y-%m-%d %H:%M:%S'

@csrf_exempt
def addConvocatoria(request):
    try:
        if request.method == 'POST':
            
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                nombre = data.get('nombre')
                idTipo = data.get('tipo')
                cantidadBeneficiarios = data.get('cantidad_beneficiarios')
                fecha_inicio_str = data.get('fecha_inicio')
                fecha_final_str = data.get('fecha_final')
                documento = None
            else:
                nombre = request.POST.get('nombre')
                idTipo = request.POST.get('tipo')
                cantidadBeneficiarios = request.POST.get('cantidad_beneficiarios')
                fecha_inicio_str = request.POST.get('fecha_inicio')
                fecha_final_str = request.POST.get('fecha_final')
                documento = request.FILES.get('documento')
            
            if not all([nombre, idTipo, cantidadBeneficiarios, fecha_inicio_str, fecha_final_str]):
                return JsonResponse({"mensaje": "Faltan campos obligatorios"}, status=400)
            
            tipo = TipoConvocatoria.objects.get(pk=idTipo)
            fecha_inicio = datetime.strptime(fecha_inicio_str, formato_fecha)
            fecha_final = datetime.strptime(fecha_final_str, formato_fecha)
            
            convocatoria = Convocatoria(
                nombre=nombre,
                tipo=tipo,
                cantidad_beneficiarios=cantidadBeneficiarios,
                fecha_inicio=fecha_inicio,
                fecha_final=fecha_final,
                documento=documento
            )
            convocatoria.save()
            
            mensaje = "Convocatoria Agregada Correctamente"
            retorno = {"mensaje": mensaje, "id": convocatoria.id}
        else:
            retorno = {"mensaje": "Método no permitido"}
    except Error as error:
        retorno = {"mensaje": f"Error de base de datos: {str(error)}"}
    except Exception as e:
        retorno = {"mensaje": f"Error: {str(e)}"}
    
    return JsonResponse(retorno)

@csrf_exempt
def addFuncionario(request):
    try:
        if request.method == 'POST':
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                identificacion = data.get('identificacion')
                nombres = data.get('nombres')
                apellidos = data.get('apellidos')
                correo = data.get('correo')
                cargo = data.get('cargo')
            else:
                identificacion = request.POST.get('identificacion')
                nombres = request.POST.get('nombres')
                apellidos = request.POST.get('apellidos')
                correo = request.POST.get('correo')
                cargo = request.POST.get('cargo')
            
            if not all([identificacion, nombres, apellidos, correo, cargo]):
                return JsonResponse({"mensaje": "Faltan campos obligatorios"}, status=400)
            
            with transaction.atomic():
                
                if User.objects.filter(username=correo).exists():
                    return JsonResponse({"mensaje": "El correo ya está registrado"}, status=400)
                
            
                usuario = User(
                    username=correo,
                    first_name=nombres,
                    last_name=apellidos,
                    email=correo,
                    is_active=True
                )
                usuario.set_password("12345")
                usuario.save()
                
                
                funcionario = Funcionario(usuario=usuario, cargo=cargo)
                funcionario.save()
                
                mensaje = "Funcionario Agregado Correctamente"
        else:
            mensaje = "Método no permitido"
    except Error as error:
        transaction.rollback()
        mensaje = f"Error de base de datos: {str(error)}"
    except Exception as e:
        mensaje = f"Error: {str(e)}"
    
    return JsonResponse({"mensaje": mensaje})

def listar_convocatorias(request):
    try:
        convocatorias = Convocatoria.objects.filter(activa=True).order_by('-fecha_registro')
        data = []
        for conv in convocatorias:
            data.append({
                'id': conv.id,
                'nombre': conv.nombre,
                'tipo': conv.tipo.nombre,
                'tipo_id': conv.tipo.id,
                'cantidad_beneficiarios': conv.cantidad_beneficiarios,
                'fecha_inicio': conv.fecha_inicio.strftime(formato_fecha),
                'fecha_final': conv.fecha_final.strftime(formato_fecha),
                'documento_url': conv.documento.url if conv.documento else None,
                'documento_nombre': conv.documento.name.split('/')[-1] if conv.documento else None,
                'activa': conv.activa
            })
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({"mensaje": f"Error: {str(e)}"}, status=500)

def listar_postulaciones(request):
    try:
        convocatoria_id = request.GET.get('convocatoria_id')
        if convocatoria_id:
            postulaciones = Postulacion.objects.filter(convocatoria_id=convocatoria_id)
        else:
            postulaciones = Postulacion.objects.all()
        
        data = []
        for post in postulaciones:
            data.append({
                'id': post.id,
                'aprendiz': f"{post.aprendiz.usuario.first_name} {post.aprendiz.usuario.last_name}",
                'aprendiz_id': post.aprendiz.id,
                'convocatoria': post.convocatoria.nombre,
                'convocatoria_id': post.convocatoria.id,
                'fecha_postulacion': post.fecha_postulacion.strftime(formato_fecha),
                'estado': post.estado,
                'puntaje': post.puntaje
            })
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({"mensaje": f"Error: {str(e)}"}, status=500)