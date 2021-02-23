import known_data


STOP_WORD = "stop"


def mob_payment():
    phrase = input("Введите сумму, карту и получателя: ")
    phrase_by_words = phrase.split()
    i = 0
    digit_check = 0
    card_check = 0
    contact_check = 0
    final_phrase = {"final_amount": "final_amount", "final_card": "final_card", "final_contact": "final_contact", "STOP_WORD": "STOP_WORD"}
    while i < len(phrase_by_words):
        if phrase_by_words[i].replace('.', '', 1).isdigit():
            final_phrase["final_amount"] = phrase_by_words[i]
            print(f"Введена сумма: {phrase_by_words[i]}")
            digit_check += 1
        elif phrase_by_words[i] == STOP_WORD:
            final_phrase["STOP_WORD"] = STOP_WORD
            break
        elif phrase_by_words[i] in known_data.cards():
            final_phrase["final_card"] = phrase_by_words[i]
            print(f"Выбрана карта: {phrase_by_words[i]}")
            card_check += 1
        elif phrase_by_words[i] in known_data.contacts():
            final_phrase["final_contact"] = phrase_by_words[i]
            print(f"Выбран номер: {phrase_by_words[i]}")
            contact_check += 1
        i += 1

    # print(phrase_by_words)   потом будет в лог инфа отправляться
    # print(final_phrase)
    # print(f"digits: {digit_check} \n cards {card_check}")  # проверка перебора списка

    if final_phrase["STOP_WORD"] == STOP_WORD:
        stop()
    elif len(phrase_by_words) < 1:
        result = "Ошибка. Данные не были введены.\n"
        test_result = "fail"
        print(result)
        return test_result
    elif digit_check > 1:
        result = "Ошибка. Введено больше 1 суммы\n"
        test_result = "fail"
        print(result)
        return test_result
    elif card_check > 1:
        result = "Ошибка. Введено больше 1 карты\n"
        test_result = "fail"
        print(result)
        return test_result
    elif contact_check > 1:
        result = "Ошибка. Введено больше 1 контакта\n"
        test_result = "fail"
        print(result)
        return test_result

    if digit_check == 0:
        amount = process_amount(input("Введите сумму: "))
        if amount == STOP_WORD:
            stop()
        else:
            print(f"Введена сумма {amount}")
            final_phrase["final_amount"] = amount

    if card_check == 0:
        card = process_voice_card(input("Выберите карту: "))
        if card == STOP_WORD:
            stop()
        else:
            print(f"Выбрана карта {card}")
            final_phrase["final_card"] = card

    if contact_check == 0:
        contact = process_voice_contact(input("Введите получателя: "))
        if contact == STOP_WORD:
            stop()
        else:
            print(f"Выбран получатель {contact}")
            final_phrase["final_contact"] = contact

    print(f"______________________________\nСумма:{final_phrase['final_amount']}\nКарта:{final_phrase['final_card']}\nПолучатель:{final_phrase['final_contact']}\n")

    try:
        final_phrase["final_amount"], final_phrase["final_card"], final_phrase["final_contact"] = confirmation(final_phrase["final_amount"], final_phrase["final_card"], final_phrase["final_contact"])
        print(f"Перевожу {final_phrase['final_amount']} с {final_phrase['final_card']} на {final_phrase['final_contact']}")
        test_result = "success"
        return test_result
    except:
        test_result = "failed"
        return test_result


def confirmation(pre_amount, pre_card, pre_contact):
    choice = "д"
    while choice.lower() != "да":
        choice = input("Все верно?")
        if choice == STOP_WORD:
            stop()
            return False
        elif choice == "изменить сумму":
            amount = process_amount(input("Введите сумму: "))
            if amount == STOP_WORD:
                stop()
                return False
            else:
                print(f"Введена сумма {amount}")
                pre_amount = amount
        elif choice == "изменить карту":
            card = process_voice_card(input("Выберите карту: "))
            if card == STOP_WORD:
                stop()
                return False
            else:
                print(f"Выбрана карта {card}")
                pre_card = card
        elif choice == "изменить номер":
            contact = process_voice_contact(input("Введите получателя: "))
            if contact == STOP_WORD:
                stop()
                return False
            else:
                print(f"Выбран получатель {contact}")
                pre_contact = contact
        elif choice == "да":
            break
        else:
            print("Повторите ввод.")
    #print(pre_amount, pre_card, pre_contact)
    return pre_amount, pre_card, pre_contact


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
    balance = known_data.balance()
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
    return voice_in in known_data.cards()  # Если утверждение возврата верное, то возвращает true


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


def is_contact_known(voice_in: str) -> bool:
    contacts = known_data.contacts()
    if voice_in in contacts:
        return True
    else:
        for value in contacts.values():
            if value == voice_in:
                return True
            else:
                return False


def process_voice_contact(voice_in: str) -> str:
    if is_contact_known(voice_in):
        contact = voice_in
        return contact
    elif is_stop(voice_in):
        return STOP_WORD
    else:
        return process_voice_contact(input("Повторите ввод получателя: "))


if __name__ == "__main__":  # Переменная __name__ указывает на имя модуля. Для главного модуля, который непосредственно
    # запускается, эта переменная всегда будет иметь значение __main__ вне зависимости от имени файла.
    # Данный подход с проверкой имени модуля является более рекомендуемым подходом, чем просто вызов метода main.
    # example()
    mob_payment()
    #confirmation(100, "visa", "mom")


