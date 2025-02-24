from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Settings, BonusBet, SecondBet
from .services import update_bets


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
        #BonusBet.objects.all().delete()
        #update_bets()
        bets = BonusBet.objects.all().order_by("-profit_index")[:int(request.GET.get('limit'))]
        for bet in bets:
            bet.profit_index *= float(bonus_size)
            bet.hedge_index *= float(bonus_size)
        return render(request, 'bonus_bets.html', {'bets' : bets, 'settings': user_settings})

    return render(request, 'bonus_bets.html', {'settings': user_settings})

@login_required
def second_chance(request):
    user_settings, created = Settings.objects.get_or_create(user=request.user)

    second_size = request.GET.get('amount')
    if second_size is not None:
        #second_size = float(second_size)
        #SecondBet.objects.all().delete()
        update_bets()
        return_rate = float(request.GET.get('return')) / 100.0
        bets = SecondBet.objects.all().order_by("-profit_index")[:int(request.GET.get("limit"))]
        print(bets[0].profit_index)
        for bet in bets:
            # we need to calculate profit and hedge from the ground up.
            # first profit
            # P = S * (Ob - (Ob + 1 - r) / (Oh + 1))
            odd_b = bet.bonus_odds / 100
            odd_h = 100 / abs(bet.hedge_odds)

            profit = second_size * (odd_b - (odd_b + 1 - return_rate) / (odd_h + 1))
            bet.profit_index = profit

            # now, hedge
            # S * ((Ob + 1 - r) / (Oh + 1))
            hedge = second_size * ((odd_b + 1 - return_rate) / (odd_h + 1))
            bet.hedge_index = hedge
        #bets.order_by("-profit_index")
        return render(request, 'second_chance.html', {'bets' : bets, 'settings': user_settings})

    return render(request, 'second_chance.html', {'settings': user_settings})

