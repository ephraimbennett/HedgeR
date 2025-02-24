import requests
import json

def calculate_all(data):
    bets = find_best_bets(data)

    bonus_bets = bonus_bet_calc(bets)
    second_bets = second_chance_calc(bets)

    return bonus_bets, second_bets



def find_best_bets(data):
    bets = []
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
        to_append = {'bonus_bet': [bet_bookie, biggest_plus], 'hedge_bet': [hedge_bookie, largest_minus]}
        to_append['title'] = event["away_team"] + " @ " + event["home_team"]
        bets.append(to_append)
    return bets

def bonus_bet_calc(bets):
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
    for bet in bets:     
        plus = bet['bonus_bet'][1]
        minus = bet['hedge_bet'][1]

        # calculate the profit index ~ (Ob - 1) x ((Oh - 1) / Oh)
        odd_b = 1 + plus / 100
        odd_h = 1 + (100 / abs(minus))
        profit_idx = (odd_b - 1) * ((odd_h - 1) / odd_h)
        print(odd_b, odd_h)
        

        hedge_index = (odd_b - 1) / odd_h
        bonus_bet = {'bonus_bet': [bet['bonus_bet'][0], plus], 'hedge_bet': [bet['hedge_bet'][0], minus, hedge_index]}
        bonus_bet['profit_index'] = profit_idx
        bonus_bet['title'] = bet['title']

        bonus_bets.append(bonus_bet)
    return bonus_bets

def second_chance_calc(bets):
    '''
    Given, ob = second chance odds, oh = hedge odds, S = second chance size, H = hedge size, r = return find profit:
    P = (S * ob) - H = (H * oh) - S + (S * r), =>
    H = ((S * ob) + S - Sr) / (oh + 1) = S * ((Ob + 1 - r) / (Oh + 1)), =>
    P = (S * ob) - ((S * ob) + S - Sr) / (oh + 1), =>
    P = S * (Ob - (Ob + 1 - r) / (Oh + 1))

    The hedge index is: ((Ob + 1 - r) / (Oh + 1))
    The profit index is: (Ob - (Ob + 1 - r) / (Oh + 1))
    '''
    second_bets = []
    for bet in bets:
        plus = bet['bonus_bet'][1]
        minus = bet['hedge_bet'][1]


        # calculate the profit index ~ (Ob - (Ob + 1 - r) / (Oh + 1)). Use r = 1 for now, then recalc later.
        odd_b = 1 + plus / 100
        odd_h = 1 + (100 / abs(minus))
        profit_idx = (odd_b - (odd_b) / (odd_h + 1))

        second_bet = {'bonus_bet': [bet['bonus_bet'][0], plus], 'hedge_bet': [bet['hedge_bet'][0], minus]}
        second_bet['profit_index'] = profit_idx
        second_bet['title'] = bet['title']
        
        second_bets.append(second_bet)
    return second_bets