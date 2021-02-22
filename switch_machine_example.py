STATES = [
    "INIT",
    "GET_AMOUNT",
    "CONFIRM",
    "STOP"
]

CONTEXT = {
    "amount": None,
    "card": None,
    "phone": None,
}


def init():
    """
    Инициализация процесса, что-то происходит
    :return:
    """
    return "GET_AMOUNT"


def get_amount():
    """
    Проверка введенной суммы, запросить ее, если суммы нет
    :return:
    """
    # TODO
    global CONTEXT
    if CONTEXT["amount"] != None:
        return "GET_CARD"
    # TODO
    if True:
        return "STOP"
    return "GET_CARD"


def get_card():
    """
    Проверка введенной карты
    :return:
    """
    # TODO
    return "GET_PHONE"


def confirm():
    """
    Поддтверждение платежа
    :return:
    """
    if True:
        CONTEXT.pop("amount")
        return "GET_AMOUNT"
    return "GOOD_BYE"


def get_phone():
    return "CONFIRM"


def process():
    """
    Функция, которая описывает граф переходов из состояний
    :return:
    """
    current_state = "INIT"
    exit_state = "STOP"
    while current_state != exit_state:
        if current_state == "INIT":
            current_state = init()
        if current_state == "GET_AMOUNT":
            current_state = get_amount()
        if current_state == "GET_CARD":
            current_state = get_card()
        if current_state == "GET_PHONE":
            current_state = get_phone()
        if current_state == "CONFIRM":
            current_state = confirm()
        if current_state == "GOOD_BYE":
            print("GOOD_BYE")
            break
    return None


if __name__ == "__main__":
    process()
