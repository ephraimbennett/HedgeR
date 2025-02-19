from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Settings, BonusBet
from .services import update_bonus_bets


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

@login_required
def bonus_bets(request):
    user_settings, created = Settings.objects.get_or_create(user=request.user)

    bonus_size = request.GET.get('amount')
    if bonus_size is not None:
        BonusBet.objects.all().delete()
        update_bonus_bets()
        bets = BonusBet.objects.all().order_by("-profit_index")[:int(request.GET.get('limit'))]
        for bet in bets:
            bet.profit_index *= float(bonus_size)
            bet.hedge_index *= float(bonus_size)
        return render(request, 'bonus_bets.html', {'bets' : bets, 'settings': user_settings})

    return render(request, 'bonus_bets.html', {'settings': user_settings})