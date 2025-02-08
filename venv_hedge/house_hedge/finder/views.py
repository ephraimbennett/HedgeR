from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Settings


# Create your views here.

@login_required
def dashboard(request):
    
    user_settings, created = Settings.objects.get_or_create(user=request.user)
    print(user_settings)

    return render(request, "dashboard.html", {
        'potential_profit': 2400,
        'settings': user_settings
    })