from django.urls import path
from . import viewsLider, viewsAprendiz, views

urlpatterns = [
    # Página principal 
    path('', views.home, name='home'),
    
    # Autenticación
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Líder de Bienestar
    path('addConvocatoria/', viewsLider.addConvocatoria, name='add_convocatoria'),
    path('addFuncionario/', viewsLider.addFuncionario, name='add_funcionario'),
    path('convocatorias/', viewsLider.listar_convocatorias, name='listar_convocatorias'),
    path('postulaciones/', viewsLider.listar_postulaciones, name='listar_postulaciones'),
    
    # Aprendiz
    path('registrar-aprendiz/', viewsAprendiz.registrar_aprendiz, name='registrar_aprendiz'),
    path('postularse/', viewsAprendiz.postularse, name='postularse'),
    path('mis-postulaciones/', viewsAprendiz.mis_postulaciones, name='mis_postulaciones'),
]