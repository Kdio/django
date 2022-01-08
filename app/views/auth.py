"""
"""

from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required

from app.forms.auth import LogInForm, MyPasswordChangeForm


class AppLoginView(LoginView):
    form_class = LogInForm
    template_name = 'auth/login.html'
    extra_context = {
        'page_title': _('Entrar no sistema')
    }

    def get_success_url(self):
        return reverse('home')


class AppLogoutView(LogoutView):
    next_page = reverse_lazy('login')


@login_required
def password(request):
    form = MyPasswordChangeForm(request.user, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)  # Important!
        messages.success(request, _('Senha alterada com sucesso'))
        next_page = reverse_lazy('home')
        return redirect('home')
    return render(request, 'auth/password.html', {'form': form})
