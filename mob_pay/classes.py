import known_data


class Card:
    def __init__(self, card):
        self.card = card

    def check_card(self) -> bool:
        if self.card in known_data.cards():
            print(f"{self.card} есть в наличии")
            return True
        else:
            self.card = input("Повторите ввод\n")
            return False

    def set_card(self, card):
        self.card = card


    def process_card(self, voice_in: str) -> str:
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
            return process_card(input("Повторите ввод карты: "))


def check():
    card = Card(input("Введите карту"))
    while not card.check_card():

        card.check_card()

check()