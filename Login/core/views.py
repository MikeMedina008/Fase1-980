# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm
from .models import UserProfile  # Importa tu modelo UserProfile
from django.utils import timezone
from datetime import timedelta

def home(request):
    return render(request, 'core/home.html')

@login_required
def products(request):
    return render(request, 'core/products.html')

def register(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data=request.POST)

        if user_creation_form.is_valid():
            user_creation_form.save()

            user = authenticate(username=user_creation_form.cleaned_data['username'], password=user_creation_form.cleaned_data['password1'])
            login(request, user)
            return redirect('home')
        else:
            data['form'] = user_creation_form

            # Incrementa el contador de intentos fallidos
            username = request.POST.get('username')
            user_profile, created = UserProfile.objects.get_or_create(user__username=username)
            user_profile.failed_login_attempts += 1
            user_profile.save()

            # Si hay 3 intentos fallidos, bloquea al usuario durante 15 minutos
            if user_profile.failed_login_attempts >= 3:
                user_profile.blocked_until = timezone.now() + timedelta(minutes=15)
                user_profile.save()
                return render(request, 'blocked.html')  # Página personalizada para usuarios bloqueados

    return render(request, 'registration/register.html', data)


