import mob_pay


def test_common_request():
    request = "100.123 visa"
    mob_pay.input = lambda x: request
    """
    переменная Input вызывает не встроенную ф-ию, а новую определенную нами. 
    В данном случае lambd'y, которая  возврашает переменная request
    """
    mob_pay.mob_payment()


test_common_request()