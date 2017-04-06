import hashlib
from app.models import Usuario


def run_registrar(request):
    if request.method == 'POST':
        email = request.POST['email']

        #verifica se o email ja esta cadastrado
        try:
            usuario = Usuario.objects.get(email=email)
        except:
            #se nao esta, cadastra o novo usuario
            nome = request.POST['nome']


            senha = request.POST['senha']
            hash_senha = hashlib.sha224(senha.encode('utf8'))
            senha = hash_senha.hexdigest()

            usuario = Usuario(nome=nome, email=email, senha=senha)
            try:
                usuario.save()
                resultado = True
            except:
                resultado = False

            return {'resultado': resultado}
        else:
            return {'resultado': False}