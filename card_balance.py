import random


def balance():
    possible_card_balance = list(range(10000))
    card_balance = random.choice(possible_card_balance)
    return card_balance

