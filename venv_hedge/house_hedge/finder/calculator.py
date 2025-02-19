import requests
import json


def bonus_bet_calc(data):
    # we need to find the max profit given the odds of both sides of a bet
    # given these variables:
    # S = bonus bet size, Ob = odds of the bonus, Oh = odds of the hedge (decimal form for both)
    # Profit (P) = S x (Ob - 1) x ((Oh - 1) / Oh)
    # to convert american odds to decimal:
    # for positive odds (+): O = 1 + (odds / 100)
    # for negative odds (-): O = 1 + (100 / odds)
    # this section of the Profit equation ~ (Ob - 1) x ((Oh - 1) / Oh) ~ stays the same for each bet size.
    # we want to maximize this number, so find the largest, Ob and the largest Oh for a given event. 

    # lets iterate through each event, and find the biggest underdog odds, and the smallest favorite odds
    # then we'll calculate the max profit and store it
    bonus_bets = []
    for event in data:
        biggest_plus = 0
        bet_bookie = hedge_bookie = ''
        largest_minus = -99999
        if len(event['bookmakers']) == 0:
            continue
        for bookie in event['bookmakers']:
            for outcome in bookie['markets'][0]['outcomes']:
                if outcome['price'] > 0: # underdog
                    if outcome['price'] > biggest_plus:
                        biggest_plus = outcome['price']
                        bet_bookie = bookie['title']
                else:
                    if outcome['price'] > largest_minus:
                        largest_minus = outcome['price']
                        hedge_bookie = bookie['title']        
        
        # calculate the profit index ~ (Ob - 1) x ((Oh - 1) / Oh)
        odd_b = 1 + biggest_plus / 100
        odd_h = 1 + (100 / abs(largest_minus))
        profit_idx = (odd_b - 1) * ((odd_h - 1) / odd_h)
        print(odd_b, odd_h)
        

        hedge_index = (odd_b - 1) / odd_h
        bonus_bet = {'bonus_bet': [bet_bookie, biggest_plus], 'hedge_bet': [hedge_bookie, largest_minus, hedge_index]}
        bonus_bet['profit_index'] = profit_idx

        bonus_bet['title'] = event["away_team"] + " @ " + event["home_team"]
        bonus_bets.append(bonus_bet)
    return bonus_bets