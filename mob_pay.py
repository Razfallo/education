import card_balance
import cards_list

# 222


def mob_payment():
    phrase = input("Введите сумму и карту: ")
    phrase_by_words = phrase.split()
    phrase_by_words.sort()
    i = 0
    digit_check = 0
    card_check = 0
    if len(phrase_by_words) < 1:
        print("Введены некорректные данные.\n")
        return None
    while i < len(phrase_by_words):
        if phrase_by_words[i].replace('.', '', 1).isdigit():
            phrase_by_words[i] = amount_check(phrase_by_words[i])
            phrase_by_words.insert(0, phrase_by_words[i])
            print("Введена сумма:", phrase_by_words[i])
            digit_check += 1
            i += 1
        elif phrase_by_words[i] == "stop":
            i = len(phrase_by_words)
            stop()
        elif str(phrase_by_words[i]) in cards_list.cards():
            phrase_by_words.insert(1, phrase_by_words[i])
            print("Выбрана карта:", phrase_by_words[i])
            i += 1
            card_check += 1
        i += 1
    print(phrase_by_words)
    print("digits:", digit_check, "\n", "cards", card_check)  # проверка перебора списка
    if digit_check == 1 and card_check == 1:
        print("Перевожу", phrase_by_words[0], "c", phrase_by_words[1])
        return None
    if digit_check > 1 or card_check > 1:
        print("Введены некорректные данные")
        return None
    elif digit_check == 0 and card_check == 1:
        amount = amount_check(input("Введите сумму: "))
        if amount == "stop":
            stop()
        else:
            print("Перевожу", amount, "c", phrase_by_words[0])
            return None
    elif digit_check == 1 and card_check == 0:
        card = card_choice(input("Выберите карту: "))
        if card == "stop":
            stop()
        else:
            print("Перевожу", phrase_by_words[0], "c", card)
            return None


def stop():
    print("До свидания\n")
    return None


def amount_check(amount):
    balance = card_balance.balance()
    try:
        amount = round(float(amount), 2)
        if amount <= balance:  # ну наверняка есть функция возвращающая баланс на карте
            return amount
        elif amount > balance:
            print("Недостаточно средств")
            return amount_check(input("Повторите ввод суммы: "))
        else:
            print("Введены некорректные данные.\n")
            return amount_check(input("Повторите ввод суммы: "))
    except ValueError:
        if str(amount) == "stop":
            return "stop"
        else:
            return amount_check(input("Повторите ввод суммы: "))


def card_choice(voice_in):
    if voice_in in cards_list.cards():
        card = voice_in
        return card
    elif voice_in == "stop":
        return "stop"
    else:
        return card_choice(input("Повторите ввод карты: "))


if __name__ == "__main__":  # Переменная __name__ указывает на имя модуля. Для главного модуля, который непосредственно
    # запускается, эта переменная всегда будет иметь значение __main__ вне зависимости от имени файла.
    # Данный подход с проверкой имени модуля является более рекомендуемым подходом, чем просто вызов метода main.
    # example()
    mob_payment()