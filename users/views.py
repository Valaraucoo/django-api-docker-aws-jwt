from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import redirect, render
from django.views import generic

from . import forms


class LoginView(generic.View):
    template_name = 'login.html'
    form_class = forms.LoginForm

    def get_context_data(self, *args, **kwargs):
        return {
            'is_authenticated': self.request.user.is_authenticated,
            'form': self.form_class,
        }

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/admin')

        context = self.get_context_data(*args, **kwargs)

        email = request.session.get('email')
        password = request.session.get('password')
        user = None

        if email and password:
            user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)
            if request.user.is_authenticated:
                messages.info(request, 'You are logged in!')
                return redirect('/admin')
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            redirect('/admin')
        context = self.get_context_data(*args, **kwargs)
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            email = data.get('email')
            password = data.get('password')
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                messages.info(request, 'Successfully loged in!')
                return redirect('/admin')
            else:
                messages.error(request, 'Try again.')
        else:
            messages.error(request, 'Try again.')
        return render(request, self.template_name, context)
