import mob_pay


def test_common_request():
    request = "100.123 visa"
    mob_pay.input = lambda x: request
    """
    переменная Input вызывает не встроенную ф-ию, а новую определенную нами. 
    В данном случае lambd'y, которая  возврашает переменная request
    """
    mob_pay.mob_payment()


def test_common_request_2():
    mob_pay.input = lambda x: "mastercard 123"
    mob_pay.mob_payment()


def test_with_rubbish():
    mob_pay.input = lambda x: "mastercard 123 rubbish"
    mob_pay.mob_payment()


def test_doubled_amount():
    step_inputs = {0: "123 123 visa", 1: "321 visa"}
    context = {"step_inputs": step_inputs, "step_number": 0}
    mob_pay.input = lambda x: _on_doubled_input(context)
    mob_pay.mob_payment()


def test_doubled_card():
    step_inputs = {0: "123 mastercard visa", 1: "321 visa"}
    context = {"step_inputs": step_inputs, "step_number": 0}
    mob_pay.input = lambda x: _on_doubled_input(context)
    mob_pay.mob_payment()


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
