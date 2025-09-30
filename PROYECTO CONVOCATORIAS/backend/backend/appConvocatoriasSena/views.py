from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Aprendiz, Funcionario

def home(request):
    return JsonResponse({
        "mensaje": "API SENA Convocatorias - Sistema de Gestión",
        "version": "1.0",
        "endpoints_disponibles": {
            "home": "/api/",
            "registrar_aprendiz": "/api/registrar-aprendiz/",
            "login": "/api/login/",
            "logout": "/api/logout/",
            "convocatorias": "/api/convocatorias/",
            "add_convocatoria": "/api/addConvocatoria/",
            "add_funcionario": "/api/addFuncionario/",
            "postularse": "/api/postularse/",
            "mis_postulaciones": "/api/mis-postulaciones/",
        }
    })

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            #rol  usuario
            rol = "Sin rol asignado"
            if hasattr(user, 'aprendiz'):
                rol = "Aprendiz"
            elif hasattr(user, 'funcionario'):
                rol = "Funcionario"
            elif user.is_superuser:
                rol = "Administrador"
            
            return JsonResponse({
                "mensaje": "Login exitoso",
                "usuario": {
                    "id": user.id,
                    "username": user.username,
                    "nombres": user.first_name,
                    "apellidos": user.last_name,
                    "email": user.email,
                    "rol": rol
                }
            })
        else:
            return JsonResponse({"mensaje": "Credenciales incorrectas"}, status=400)
    else:
        return JsonResponse({"mensaje": "Método no permitido"}, status=405)

@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({"mensaje": "Logout exitoso"})