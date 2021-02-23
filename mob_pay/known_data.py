import random


def balance():
    possible_card_balance = list(range(10000))
    card_balance = random.choice(possible_card_balance)
    return card_balance


def cards():
    cards = ["visa", "mastercard", "maestro"]
    return cards


def contacts():
    contacts = {"mom": "89031234567", "bro": "+79051234567"}
    return contacts
