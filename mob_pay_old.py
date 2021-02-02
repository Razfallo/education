import card_balance
import cards_list


def mob_payment():
    phrase = input("Введите сумму и карту: ")
    phrase_by_words = phrase.split()
    phrase_by_words.sort()
    i = 0
    digit_check = 0
    card_check = 0
    final_phrase = {"final_amount": "final_amount", "final_card": "final_card"}
    if len(phrase_by_words) < 1:
        print("Введены некорректные данные.\n")
        return None
    while i < len(phrase_by_words):
        if phrase_by_words[i].replace('.', '', 1).isdigit():
            final_phrase["final_amount"] = phrase_by_words[i]
            print("Введена сумма:", phrase_by_words[i])
            digit_check += 1
        elif phrase_by_words[i] == "stop":
            stop()
            break
        elif str(phrase_by_words[i]) in cards_list.cards():
            final_phrase["final_card"] = phrase_by_words[i]
            print("Выбрана карта:", phrase_by_words[i])
            card_check += 1
        i += 1
    print(phrase_by_words)
    print(final_phrase)
    print("digits:", digit_check, "\n", "cards", card_check)  # проверка перебора списка
    if digit_check == 1 and card_check == 1:
        print("Перевожу", final_phrase["final_amount"], "c", final_phrase["final_card"])
        return None
    if digit_check > 1 or card_check > 1:
        print("Введены некорректные данные")
        return None
    elif digit_check == 0 and card_check == 1:
        amount = amount_inbalance(input("Введите сумму: "))
        if amount == "stop":
            stop()
        else:
            print("Перевожу", amount, "c", phrase_by_words[0])
            return None
    elif digit_check == 1 and card_check == 0:
        card = card_isknown(input("Выберите карту: "))
        if card == "stop":
            stop()
        else:
            print("Перевожу", amount_inbalance(phrase_by_words[0]), "c", card)
            return None


def stop():
    print("До свидания\n")
    return None


def amount_inbalance(amount):
    balance = card_balance.balance()
    try:
        amount = round(float(amount), 2)
        if amount <= balance:  # ну наверняка есть функция возвращающая баланс на карте
            return amount
        elif amount > balance:
            print("Недостаточно средств")
            return amount_inbalance(input("Повторите ввод суммы: "))
        else:
            print("Введены некорректные данные.\n")
            return amount_inbalance(input("Повторите ввод суммы: "))
    except ValueError:
        if str(amount) == "stop":
            return "stop"
        else:
            return amount_inbalance(input("Повторите ввод суммы: "))


def card_isknown(voice_in):
    if voice_in in cards_list.cards():
        card = voice_in
        return card
    elif voice_in == "stop":
        return "stop"
    else:
        return card_isknown(input("Повторите ввод карты: "))


if __name__ == "__main__":  # Переменная __name__ указывает на имя модуля. Для главного модуля, который непосредственно
    # запускается, эта переменная всегда будет иметь значение __main__ вне зависимости от имени файла.
    # Данный подход с проверкой имени модуля является более рекомендуемым подходом, чем просто вызов метода main.
    # example()
    mob_payment()