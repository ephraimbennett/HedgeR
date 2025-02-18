from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Settings

from .forms import SettingsForm


# Create your views here.

@login_required
def dashboard(request):
    
    user_settings, created = Settings.objects.get_or_create(user=request.user)
    print(user_settings)

    return render(request, "dashboard.html", {
        'potential_profit': 2400,
        'settings': user_settings
    })

@login_required
def settings(request):
    user_settings, created = Settings.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = SettingsForm(request.POST, instance=user_settings)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = SettingsForm(instance=user_settings)
    return render(request, 'settings.html', {'form' : form})