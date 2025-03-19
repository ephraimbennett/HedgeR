from .models import BonusBet, SecondBet, BookMaker, Promo
from .calculator import calculate_all
from datetime import timezone



from django.utils.dateparse import parse_datetime

from .scrape.sportsbookreview import scrape_sportsbookreview

import requests

def update_bets():
    # clear existing tables
    SecondBet.objects.all().delete()
    BonusBet.objects.all().delete()
    BookMaker.objects.all().delete()

    # get the data, will change later obviously
    key_api = "1fcbe0cddc5a8bbf56e301cb2a949d4a"
    url_sports = f"https://api.the-odds-api.com/v4/sports?apiKey={key_api}"
    response = requests.get(url=url_sports)
    sports_names = response.json()
    keys = []

    for item in sports_names:
        keys.append(item['key'])

    # get main lines
    domain = "https://api.the-odds-api.com/v4/sports/"
    keys =  ["basketball_nba", "baseball_ncaa", "basketball_ncaab", "basketball_wncaab", "boxing_boxing",
             "icehockey_nhl"]
    markets = ["h2h", "totals", "spreads"]
    data = []
    for market in markets:
        for key in keys:
            url_odds = f"{domain}{key}/odds?regions=us&oddsFormat=american&apiKey={key_api}&markets={market}"
            response = requests.get(url=url_odds)
            data.extend(response.json())
    bets, second_bets = calculate_all(data)

    # have a set of the names of bookmakers, as we go through the bets, add to this set.
    bookmakers = set()

    print(len(bets))
    for bet in bets:
        bookmakers.add(bet['bonus_bet'][0])
        bookmakers.add(bet['hedge_bet'][0])

        bet_model = BonusBet(title=bet['title'], bonus_bet=bet['bonus_bet'][0], hedge_bet=bet['hedge_bet'][0])
        bet_model.bonus_odds = bet['bonus_bet'][1]
        bet_model.hedge_odds = bet['hedge_bet'][1]
        bet_model.hedge_index = bet['hedge_bet'][3]
        bet_model.profit_index = bet['profit_index']
        bet_model.hedge_name = bet['hedge_bet'][2]
        bet_model.bonus_name = bet['bonus_bet'][2]
        bet_model.market = bet['market']
        bet_model.sport = bet['sport']
        bet_model.time = bet['time']

        bet_model.save()

    for bet in second_bets:
        bookmakers.add(bet['bonus_bet'][0])
        bookmakers.add(bet['hedge_bet'][0])

        bet_model = SecondBet(title=bet['title'], bonus_bet=bet['bonus_bet'][0], hedge_bet=bet['hedge_bet'][0])
        bet_model.bonus_odds = bet['bonus_bet'][1]
        bet_model.hedge_odds = bet['hedge_bet'][1]
        bet_model.bonus_name = bet['bonus_bet'][2]
        bet_model.hedge_name = bet['hedge_bet'][2]
        bet_model.profit_index = bet['profit_index']
        bet_model.market = bet['market']
        bet_model.sport = bet['sport']
        bet_model.time = bet['time']

        bet_model.save()

    for b in bookmakers:
        book_model = BookMaker(title=b)
        book_model.save()

def update_promos():
    # clear existing promos
    Promo.objects.all().delete()

    url = "https://www.sportsbookreview.com/bonuses/"
    promos = scrape_sportsbookreview(url)

    for promo in promos:
        model = Promo(bookmaker=promo[0], description=promo[1], code=promo[2])
        if len(promo) == 4:
            model.url = promo[3]
        else:
            model.url = '/'
        model.save()
