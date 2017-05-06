from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from actions._login import run_login
from actions._usuario_registrar import run_usuario_registrar
from actions._sair import run_sair

from classes.util import *



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
            return render(request, 'users/login.html', context)
    else:
        return render(request, 'users/login.html', {})


def registrar(request):
    if request.method == 'POST':
        context = run_usuario_registrar(request)

        if context['resultado']:
            return HttpResponseRedirect(reverse('users:login'))#render(request, 'users/login.html', {})
        else:
            return render(request, 'users/usuario_registrar.html', {})
    else:
        return render(request, 'users/usuario_registrar.html', {})


def sair(request):
    context = run_sair(request)

    return HttpResponseRedirect(reverse('users:login'))