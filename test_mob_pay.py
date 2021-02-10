import mob_pay


def test_result(result: str):
    if result == "success" or "fail":
        print("\nТест успешен\n")
    else:
        print("\nТест провален\n")


def test_common_request():
    print("______________________________\nСтандартный ввод\n______________________________")
    request = "100.123 visa"
    mob_pay.input = lambda x: request
    """
    переменная Input вызывает не встроенную ф-ию, а новую определенную нами. 
    В данном случае lambd'y, которая  возврашает переменная request
    """
    test_result(mob_pay.mob_payment())


def test_common_request_2():
    print("______________________________\nСтандартный ввод №2\n______________________________")
    mob_pay.input = lambda x: "mastercard 123"
    test_result(mob_pay.mob_payment())


def test_with_no_input():
    print("______________________________\nПустой ввод\n______________________________")
    mob_pay.input = lambda x: " "
    test_result(mob_pay.mob_payment())


def test_with_rubbish():
    print("______________________________\nВвод с <мусором>\n______________________________")
    mob_pay.input = lambda x: "mastercard 123 rubbish"
    test_result(mob_pay.mob_payment())


def test_doubled_amount():
    print("______________________________\nВвод с 2мя суммами\n______________________________")
    step_inputs = {0: "123 123 visa", 1: "321 visa"}
    context = {"step_inputs": step_inputs, "step_number": 0}
    mob_pay.input = lambda x: _on_doubled_input(context)
    test_result(mob_pay.mob_payment())


def test_doubled_card():
    print("______________________________\nВвод с 2мя картами\n______________________________")
    step_inputs = {0: "123 mastercard visa", 1: "321 visa"}
    context = {"step_inputs": step_inputs, "step_number": 0}
    mob_pay.input = lambda x: _on_doubled_input(context)
    test_result(mob_pay.mob_payment())


def _on_doubled_input(context: dict) -> str:
    step_number = context["step_number"]
    if step_number > 2:
        raise ValueError(step_number)

    result = context["step_inputs"][step_number]
    context["step_number"] += 1
    return result


if __name__ == "__main__":
    test_common_request()
    test_common_request_2()
    test_with_rubbish()
    test_doubled_amount()
    test_doubled_card()



