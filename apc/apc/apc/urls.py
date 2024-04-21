from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from clinica import views

#Comandos: py manage.py makemigrations migrate runserver

urlpatterns = [
    
#-------------------------------------------------USUARIO--------------------------------------------------------------------#    
    path(''         					  , views.login,      name="login"),
    path('usuario'  					  , views.usuario,    name="usuario"),
    path('login'    					  , views.login,      name="login"),
    path('sair'     					  , views.sair,       name="sair"),
    path('admin/'                         , admin.site.urls),
#-------------------------------------------------MEDICOS--------------------------------------------------------------------#     
    path('medico'   					  , views.medico,     name="medico"),
    path('horario'  					  , views.horario,    name="horario"),
    path('consultam'					  , views.consultam,  name="consultam"),
    path('consultau'					  , views.consultau,  name="consultau"),
    path('finalizar/<int:id_consulta>'    , views.finalizar , name="finalizar"), 
    path('anexar/<int:id_consulta>/'      , views.anexar,     name="anexar"),
#-------------------------------------------------PACIENTE-------------------------------------------------------------------#
    path('home'     					  , views.home,       name="home"),
    path('minhas/'                        , views.minhas,     name="minhas"), 
    path('escolher/<int:id_dados_medicos>', views.escolher,   name="escolher"),
    path('agendar/<int:id_data_aberta>'   , views.agendar,    name="agendar"),
    path('mostrar/<int:id_consulta>/'     , views.mostrar,    name="mostrar"), 
#----------------------------------------------------------------------------------------------------------------------------# 
   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)