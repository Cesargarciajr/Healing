from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages 
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from .models import DadosMedico, Especialidades, is_medico, DatasAbertas, Consulta, Documento

#-------------------------------------------------USUARIO--------------------------------------------------------------------# 

def usuario(request):
   if request.method == "GET":
      return render(request, 'usuario.html')
   elif request.method == "POST":
      username = request.POST.get('username')
      email = request.POST.get("email")
      senha = request.POST.get("senha")
      confirmar_senha = request.POST.get('confirmar_senha')
      users = User.objects.filter(username=username)

      if users.exists(): #testa se o usuario existe
         messages.add_message( request, constants.ERROR, 'Usuario Existente')
         return redirect('usuario')
      if senha != confirmar_senha:
         messages.add_message( request, constants.ERROR, 'Senhas invalidas')
         return redirect('usuario')
      if len(senha) < 6:
         messages.add_message( request, constants.ERROR, 'Senhas menores que 6 posições')
         return redirect('usuario')
   
      try:
         User.objects.create_user(username=username, email=email, password=senha  )
         return redirect('login')
      except:
         print('Erro 4')
         return redirect('usuario')
   
def login(request):
   if request.method == "GET":
      return render(request, 'login.html')
   elif request.method == "POST":
      username = request.POST.get('username')
      senha = request.POST.get("senha")
      user = auth.authenticate(request, username=username, password=senha)
      if user:
         auth.login(request, user)
         return redirect('usuario') #temporario
         #return redirect('home') #a ser criado
      messages.add_message(request, constants.ERROR, 'Usuário ou senha incorretos')
      return redirect('login')
  
def sair(request):
   auth.logout(request)   #request.user.authenticate ou request.user ou request.user.email
   return redirect('login')

def escolher(request, id_dados_medicos):
    if request.method == "GET":
        medico = DadosMedico.objects.get(id=id_dados_medicos)
        datas_abertas = DatasAbertas.objects.filter(user=medico.user).filter(data__gte=datetime.now()).filter(agendado=False)
        return render(request, 'escolher.html', {'medico': medico, 'datas_abertas': datas_abertas})
     
#-------------------------------------------------MEDICO---------------------------------------------------------------------# 
@login_required
def medico(request):  
    
    if is_medico(request.user): 
        messages.add_message(request, constants.WARNING, 'Você já está cadastrado como médico.')
        return redirect('horario')      

    if request.method == "GET":
        especialidades = Especialidades.objects.all()
        return render(request, 'medico.html', {'especialidades' : especialidades})
    elif request.method == "POST":
        crm = request.POST.get('crm')
        nome = request.POST.get('nome')
        cep = request.POST.get('cep')
        rua = request.POST.get('rua')
        bairro = request.POST.get('bairro')
        numero = request.POST.get('numero')
        cim = request.FILES.get('cim')
        rg = request.FILES.get('rg')
        foto = request.FILES.get('foto')
        especialidade = request.POST.get('especialidade')
        descricao = request.POST.get('descricao')
        valor_consulta = request.POST.get('valor_consulta')   
        
        dados_medico = DadosMedico(crm=crm,nome=nome,cep=cep,rua=rua,bairro=bairro,numero=numero,rg=rg,cedula_identidade_medica=cim,foto=foto,user=request.user, descricao=descricao, especialidade_id=especialidade, valor_consulta=valor_consulta )
        dados_medico.save()
        messages.add_message(request, constants.SUCCESS, 'Cadastro médico realizado com sucesso.')
        return redirect('horario')
         
@login_required
def horario(request):

    if not is_medico(request.user):
        messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar essa página.')
        return redirect('sair')

    if request.method == "GET":
        dados_medicos = DadosMedico.objects.get(user=request.user)
        datas_abertas = DatasAbertas.objects.filter(user=request.user)
        return render(request, 'horario.html', {'dados_medicos': dados_medicos, 'datas_abertas': datas_abertas})
                      
    elif request.method == "POST":
        data = request.POST.get('data')
        data_formatada = datetime.strptime(data, "%Y-%m-%dT%H:%M")
        
        if data_formatada <= datetime.now():
            messages.add_message(request, constants.WARNING, 'A data deve ser maior ou igual a data atual.')
            return redirect('horario')


        horario_abrir = DatasAbertas( data=data, user=request.user    )
        horario_abrir.save()

        messages.add_message(request, constants.SUCCESS, 'Horário cadastrado com sucesso.')
        return redirect('horario')
    
def consultam(request):
    
    if not is_medico(request.user):
        messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar essa página.')
        return redirect('sair')

    hoje = datetime.now().date()
    consultas_hoje = Consulta.objects.filter(data_aberta__user=request.user).filter(data_aberta__data__gte=hoje).filter(data_aberta__data__lt=hoje + timedelta(days=1))
    consultas_restantes = Consulta.objects.exclude(id__in=consultas_hoje.values('id'))
    return render(request, 'consultam.html', {'consultas_hoje': consultas_hoje, 'consultas_restantes': consultas_restantes, 'is_medico': is_medico(request.user)})
   
def finalizar(request, id_consulta):
    
    if not is_medico(request.user):
        messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar essa página.')
        return redirect('sair')  
    
    consulta = Consulta.objects.get(id=id_consulta)
    
    if  request.user != consulta.data_aberta.user:
        messages.add_message(request, constants.WARNING, 'Esta consulta não é sua!')
    else:
        consulta.status = 'F'
        consulta.save()
        
    return redirect(f'horario') #redirect formatado 

def anexar(request, id_consulta):
    
    if not is_medico(request.user):
        messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar essa página.')
        return redirect('sair')
    
    consulta = Consulta.objects.get(id=id_consulta)
    if consulta.data_aberta.user != request.user:
        messages.add_message(request, constants.ERROR, 'Essa consulta não é sua!')
        return redirect(f'consultam/{id_consulta}')
    
    titulo = request.POST.get('titulo')
    documento = request.FILES.get('documento') #buscando o documento fornecido
    
    if not documento:
        messages.add_message(request, constants.WARNING, 'Adicione o documento.')
        return redirect(f'consultam/{id_consulta}')
    
    documento = Documento( consulta=consulta, titulo=titulo, documento=documento  )
    documento.save()
    messages.add_message(request, constants.SUCCESS, 'Documento enviado com sucesso!')
    return redirect(f'consultam/{id_consulta}')   
              
#-------------------------------------------------PACIENTE-------------------------------------------------------------------#

def home(request):
 
    if request.method == "GET":
        
        medico_filtrar = request.GET.get('medico')
        especialidades_filtrar = request.GET.getlist('especialidades')
        medicos = DadosMedico.objects.all()
        
        if medico_filtrar:
            medicos = medicos.filter(nome__icontains = medico_filtrar)
            
        if especialidades_filtrar:
            medicos = medicos.filter(especialidade_id__in=especialidades_filtrar)    
            
        especialidades = Especialidades.objects.all()
        return render(request, 'home.html', {'medicos': medicos, 'especialidades': especialidades})
    
def agendar(request, id_data_aberta):
    
    if request.method == "GET":
        data_aberta = DatasAbertas.objects.get(id=id_data_aberta)
        
        horario_agendado = Consulta(  paciente=request.user,  data_aberta=data_aberta  )
        horario_agendado.save()

        data_aberta.agendado = True
        data_aberta.save()
        
        messages.add_message(request, constants.SUCCESS, 'Horário agendado com sucesso.')
        return redirect('/pacientes/consultas/')     

def consultau(request):
    
    if request.method == "GET":

        consultas = Consulta.objects.filter(paciente=request.user).filter(data_aberta__data__gte=datetime.now())
        return render(request, 'consultau.html', {'consultas': consultas})
    
def minhas(request):
    
    if request.method == "GET":

        minhas = Consulta.objects.filter(paciente=request.user).filter(data_aberta__data__gte=datetime.now())
        return render(request, 'minhas.html', {'minhas': minhas, 'is_medico': is_medico(request.user)})

def mostrar(request, id_consulta):
    
    if request.method == 'GET':
        consulta    = Consulta.objects.get(id=id_consulta) # user medico veja models foreign key
        documentos  = Documento.objects.filter(consulta=consulta)
        dado_medico = DadosMedico.objects.get(user=consulta.data_aberta.user) # user medico veja models foreign key
        return render(request, 'mostrar.html', {'consulta': consulta, 'dado_medico': dado_medico,  'documento': documentos, 'is_medico': is_medico(request.user)})
 
 
#----------------------------------------------------------------------------------------------------------------------------#
