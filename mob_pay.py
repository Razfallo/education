import card_balance
import cards_list

STOP_WORD = "stop"


def mob_payment():
    phrase = input("Введите сумму и карту: ")
    phrase_by_words = phrase.split()
    phrase_by_words.sort()
    i = 0
    digit_check = 0
    card_check = 0
    final_phrase = {"final_amount": "final_amount", "final_card": "final_card", "STOP_WORD": "STOP_WORD"}
    if len(phrase_by_words) < 1:
        print("Введены некорректные данные.\n")
        return None
    while i < len(phrase_by_words):
        if phrase_by_words[i].replace('.', '', 1).isdigit():
            final_phrase["final_amount"] = phrase_by_words[i]
            print(f"Введена сумма: {phrase_by_words[i]}")
            digit_check += 1
        elif phrase_by_words[i] == STOP_WORD:
            final_phrase["STOP_WORD"] = STOP_WORD
            break
        elif str(phrase_by_words[i]) in cards_list.cards():
            final_phrase["final_card"] = phrase_by_words[i]
            print(f"Выбрана карта: {phrase_by_words[i]}")
            card_check += 1
        i += 1
    print(phrase_by_words)
    print(final_phrase)
    print(f"digits: {digit_check} \n {cards} card_check")  # проверка перебора списка
    if final_phrase["STOP_WORD"] == STOP_WORD:
        stop()
    elif digit_check == 1 and card_check == 1:
        print(f"Перевожу {final_phrase[0]} c {final_phrase[1]}")
        return None
    elif digit_check == 0 and card_check == 1:
        amount = process_amount(input("Введите сумму: "))
        if amount == STOP_WORD:
            stop()
        else:
            print(f"Перевожу {amount} c {phrase_by_words[0]}")
            return None
    elif digit_check == 1 and card_check == 0:
        card = process_voice_card(input("Выберите карту: "))
        if card == STOP_WORD:
            stop()
        else:
            print(f"Перевожу {process_amount(phrase_by_words[0])} c {card}")
            return None
    else:
        print("Введены некорректные данные")
        return mob_payment()


def is_stop(word: str) -> bool:
    return word == STOP_WORD


def stop():
    print("До свидания\n")
    return None


def is_float(word: str) -> bool:
    try:
        float(word)
        return True
    except ValueError:
        return False


def convert_to_float(word: str) -> float:
    """
    Convert string to float with rounding a number to 2 decimal digits.
    :param word:
    :return: decimal
    :raise ValueError: if word can not be converted
    """
    return round(float(word), 2)


def is_amount_in_balance(amount: float) -> bool:
    balance = card_balance.balance()
    amount = round(float(amount), 2)
    if amount <= balance:
        return True
    else:
        return False


def process_amount(str_amount: str):
    if is_stop(str_amount):
        return STOP_WORD

    if not is_float(str_amount):
        print("Введены некорректные данные.\n")
        return process_amount(input("Повторите ввод суммы: "))

    amount = convert_to_float(str_amount)

    if is_amount_in_balance(amount):
        return amount
    else:
        print("Недостаточно средств")
        return process_amount(input("Повторите ввод суммы: "))


def is_card_known(voice_in: str) -> bool:
    return voice_in in cards_list.cards()  # Если утверждение возврата верное, то возвращает true


def process_voice_card(voice_in: str) -> str:
    """
    def fun_name(arg: arg_type) -> fun_type
    arg_type - определил тип приходящего аргумента в функцию
    fun_type - тип возвращаемого значения функцией
    """
    if is_card_known(voice_in):
        card = voice_in
        return card
    elif is_stop(voice_in):
        return STOP_WORD
    else:
        return process_voice_card(input("Повторите ввод карты: "))


if __name__ == "__main__":  # Переменная __name__ указывает на имя модуля. Для главного модуля, который непосредственно
    # запускается, эта переменная всегда будет иметь значение __main__ вне зависимости от имени файла.
    # Данный подход с проверкой имени модуля является более рекомендуемым подходом, чем просто вызов метода main.
    # example()
    mob_payment()
