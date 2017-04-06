from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from actions._login import run_login
from actions._registrar import run_registrar

from classes._util import *



def login(request):
    #print(request.session.get('sessao_hash', 'nem tem'))

    if request.method == 'POST':
        context = run_login(request)

        if context['resultado']:
            response = HttpResponseRedirect(reverse('app:index'))

            request.session['sessao_hash'] = context['sessao_hash']
            request.session['usuario_id'] = context['usuario_id']
            return response
        else:
            return render(request, 'users/login.html', {})
    else:
        return render(request, 'users/login.html', {})


def registrar(request):
    if request.method == 'POST':
        context = run_registrar(request)

        if context['resultado']:
            return HttpResponseRedirect(reverse('users:login'))#render(request, 'users/login.html', {})
        else:
            return render(request, 'users/registrar.html', {})
    else:
        return render(request, 'users/registrar.html', {})