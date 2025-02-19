from .models import BonusBet
from .calculator import bonus_bet_calc

import requests

def update_bonus_bets():
    # get the data, will change later obviously
    key_api = "1fcbe0cddc5a8bbf56e301cb2a949d4a"
    url_sports = f"https://api.the-odds-api.com/v4/sports?apiKey={key_api}"
    response = requests.get(url=url_sports)
    sports_names = response.json()
    keys = []

    for item in sports_names:
        keys.append(item['key'])

    sport_key = "basketball_ncaab"
    url_odds = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds?regions=us&oddsFormat=american&apiKey={key_api}"

    response = requests.get(url=url_odds)
    data = response.json()

    bets = bonus_bet_calc(data)

    for bet in bets:
        bet_model = BonusBet(title=bet['title'], bonus_bet=bet['bonus_bet'][0], hedge_bet=bet['hedge_bet'][0])
        bet_model.bonus_odds = bet['bonus_bet'][1]
        bet_model.hedge_odds = bet['hedge_bet'][1]
        bet_model.hedge_index = bet['hedge_bet'][2]
        bet_model.profit_index = bet['profit_index']
        bet_model.save()