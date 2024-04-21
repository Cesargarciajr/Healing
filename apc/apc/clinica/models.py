from django.shortcuts import render, redirect
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

#-------------------------------------------------MEDICOS--------------------------------------------------------------------# 
class Especialidades(models.Model):
    especialidade = models.CharField(max_length=100)
    icone = models.ImageField(upload_to="icones", null=True, blank=True)

    def __str__(self):
	    return self.especialidade

class DadosMedico(models.Model):
    crm = models.CharField(max_length=30)
    nome = models.CharField(max_length=100)
    cep = models.CharField(max_length=15)
    rua = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    numero = models.IntegerField()
    rg = models.ImageField(upload_to="rgs")
    cedula_identidade_medica = models.ImageField(upload_to='cim')
    foto = models.ImageField(upload_to="fotos_perfil")
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    descricao = models.TextField(null=True, blank=True)
    especialidade = models.ForeignKey(Especialidades, on_delete=models.DO_NOTHING, null=True, blank=True)
    valor_consulta = models.FloatField(default=100)

    def __str__(self):
        return self.user.username

class DatasAbertas(models.Model):
    data = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    agendado = models.BooleanField(default=False)

    def __str__(self):
        return str(self.data)

#-------------------------------------------------PACIENTE-------------------------------------------------------------------# 
class Consulta(models.Model):
    status_choices = ( ('A', 'Agendada'), ('F', 'Finalizada'), ('C', 'Cancelada'), ('I', 'Iniciada')    )
    
    paciente    = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    data_aberta = models.ForeignKey(DatasAbertas, on_delete=models.DO_NOTHING)
    
    status = models.CharField(max_length=1, choices=status_choices, default='A')
    link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.paciente.username

class Documento(models.Model):
    consulta = models.ForeignKey(Consulta, on_delete=models.DO_NOTHING)
    titulo = models.CharField(max_length=30)
    documento = models.FileField(upload_to='documentos')

    def __str__(self):
        return self.titulo

#-------------------------------------------------EXTRAS---------------------------------------------------------------------#     
def is_medico(user):
    return DadosMedico.objects.filter(user=user).exists()

@property
def proxima_data(self):
    proxima_data = DatasAbertas.objects.filter(user=self.user).filter(data__gt=datetime.now()).filter(agendado=False).order_by('data').first()
    return proxima_data
    