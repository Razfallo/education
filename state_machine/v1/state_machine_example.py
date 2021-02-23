from typing import List, Any, Optional, Dict

import known_data
import mob_pay
from state_machine import State, Context


def process_voice_contact(param):
    return mob_pay.process_voice_contact(param)


def process_amount(param):
    return mob_pay.process_amount(param)


def process_voice_card(param):
    return mob_pay.process_voice_card(param)


class MobilePaymentContext(Context):
    phrase_by_words: List[str]
    final_phrase: Dict[str, Optional[Any]] = {
        "final_amount": None,
        "final_card": None,
        "final_contact": None,
        "STOP_WORD": None
    }
    digit_check = 0
    card_check = 0
    contact_check = 0
    error_message: str = None


class InitialState(State):
    """
    Первое состояние, куда впервые попадает запрос
    Инициализация сценария: Оплата телефона
    """
    context: MobilePaymentContext

    def handle_request(self):
        print(f"{self.__class__.__name__} handles request")
        phrase = input("Введите сумму, карту и получателя: ")
        phrase_by_words = phrase.split()
        self.context.phrase_by_words = phrase_by_words
        print(f"{self.__class__.__name__} changes state")
        self.context.change_state(ProcessingEnteredDataState())
        self.context.run()


class ProcessingEnteredDataState(State):
    """
    Проверка веденных данных
    Дозапрос, если что-то отсутствует
    """

    context: MobilePaymentContext

    def handle_request(self):
        print(f"{self.__class__.__name__} handles request")
        i = 0
        while i < len(self.context.phrase_by_words):
            if self.context.phrase_by_words[i].replace('.', '', 1).isdigit():
                self.context.final_phrase["final_amount"] = self.context.phrase_by_words[i]
                print(f"Введена сумма: {self.context.phrase_by_words[i]}")
                self.context.digit_check += 1
            elif self.context.phrase_by_words[i] == known_data.STOP_WORD:
                self.context.final_phrase["STOP_WORD"] = known_data.STOP_WORD
                print("Введено слово stop")
                print(f"{self.__class__.__name__} changes state")
                self.context.change_state(ExitViaStopWordState())
                return self.context.run()
            elif self.context.phrase_by_words[i] in known_data.cards():
                self.context.final_phrase["final_card"] = self.context.phrase_by_words[i]
                print(f"Выбрана карта: {self.context.phrase_by_words[i]}")
                self.context.card_check += 1
            elif self.context.phrase_by_words[i] in known_data.contacts():
                self.context.final_phrase["final_contact"] = self.context.phrase_by_words[i]
                print(f"Выбран номер: {self.context.phrase_by_words[i]}")
                self.context.contact_check += 1
            i += 1

        if self.context.final_phrase["STOP_WORD"] == known_data.STOP_WORD:
            print(f"{self.__class__.__name__} changes state")
            self.context.change_state(ExitViaStopWordState())
            return self.context.run()
        elif len(self.context.phrase_by_words) < 1:
            result = "Ошибка. Данные не были введены."
            print(f"{self.__class__.__name__} changes state")
            self.context.error_message = result
            self.context.change_state(ExitWithMessageState())
            return self.context.run()
        elif self.context.digit_check > 1:
            result = "Ошибка. Введено больше 1 суммы\n"
            print(f"{self.__class__.__name__} changes state")
            self.context.error_message = result
            self.context.change_state(ExitWithMessageState())
            return self.context.run()
        elif self.context.card_check > 1:
            result = "Ошибка. Введено больше 1 карты\n"
            print(f"{self.__class__.__name__} changes state")
            self.context.error_message = result
            self.context.change_state(ExitWithMessageState())
            return self.context.run()
        elif self.context.contact_check > 1:
            result = "Ошибка. Введено больше 1 контакта\n"
            print(f"{self.__class__.__name__} changes state")
            self.context.error_message = result
            self.context.change_state(ExitWithMessageState())
            return self.context.run()

        if self.context.digit_check == 0:
            amount = process_amount(input("Введите сумму: "))
            if amount == known_data.STOP_WORD:
                print(f"{self.__class__.__name__} changes state")
                self.context.change_state(ExitViaStopWordState())
                return self.context.run()
            else:
                print(f"Введена сумма {amount}")
                self.context.final_phrase["final_amount"] = amount

        if self.context.card_check == 0:
            card = process_voice_card(input("Выберите карту: "))
            if card == known_data.STOP_WORD:
                print(f"{self.__class__.__name__} changes state")
                self.context.change_state(ExitViaStopWordState())
                return self.context.run()
            else:
                print(f"Выбрана карта {card}")
                self.context.final_phrase["final_card"] = card

        if self.context.contact_check == 0:
            contact = process_voice_contact(input("Введите получателя: "))
            if contact == known_data.STOP_WORD:
                print(f"{self.__class__.__name__} changes state")
                self.context.change_state(ExitViaStopWordState())
                return self.context.run()
            else:
                print(f"Выбран получатель {contact}")
                self.context.final_phrase["final_contact"] = contact

        print(f"{self.__class__.__name__} changes state")
        self.context.change_state(ConfirmationState())
        return self.context.run()


class ConfirmationState(State):
    """
    Подтвеждение оплаты
    """

    context: MobilePaymentContext

    def handle_request(self):
        print(f"{self.__class__.__name__} handles request")
        self.context.final_phrase["final_amount"], self.context.final_phrase["final_card"], self.context.final_phrase[
            "final_contact"] = self.confirmation(self.context.final_phrase["final_amount"],
                                                 self.context.final_phrase["final_card"],
                                                 self.context.final_phrase["final_contact"])
        print(
            f"Перевожу {self.context.final_phrase['final_amount']} с {self.context.final_phrase['final_card']} на "
            f"{self.context.final_phrase['final_contact']}")

    def confirmation(self, pre_amount, pre_card, pre_contact):
        choice = "д"
        while choice.lower() != "да":
            choice = input("Все верно?")
            if choice == known_data.STOP_WORD:
                print(f"{self.__class__.__name__} changes state")
                return self.context.change_state(ExitViaStopWordState())
            elif choice == "изменить сумму":
                amount = process_amount(input("Введите сумму: "))
                if amount == known_data.STOP_WORD:
                    print(f"{self.__class__.__name__} changes state")
                    return self.context.change_state(ExitViaStopWordState())
                else:
                    print(f"Введена сумма {amount}")
                    pre_amount = amount
            elif choice == "изменить карту":
                card = process_voice_card(input("Выберите карту: "))
                if card == known_data.STOP_WORD:
                    print(f"{self.__class__.__name__} changes state")
                    return self.context.change_state(ExitViaStopWordState())
                else:
                    print(f"Выбрана карта {card}")
                    pre_card = card
            elif choice == "изменить номер":
                contact = process_voice_contact(input("Введите получателя: "))
                if contact == known_data.STOP_WORD:
                    print(f"{self.__class__.__name__} changes state")
                    return self.context.change_state(ExitViaStopWordState())
                else:
                    print(f"Выбран получатель {contact}")
                    pre_contact = contact
            elif choice == "да":
                break
            else:
                print("Повторите ввод.")
        return pre_amount, pre_card, pre_contact


class ExitViaStopWordState(State):
    """
    Выход по ключевому слову - stop
    """

    context: MobilePaymentContext

    def handle_request(self):
        print(f"{self.__class__.__name__} handles request")
        print("До свидания\n")


class ExitWithMessageState(State):
    """
    Отправляет сообщение, завершает процесс
    """
    context: MobilePaymentContext

    def handle_request(self):
        print(f"{self.__class__.__name__} handles request")
        message = self.context.error_message or "Что-то пошло не так"
        print(message)


def start_mobile_payment():
    init_state = InitialState()
    context = MobilePaymentContext(init_state)
    context.run()


if __name__ == "__main__":
    start_mobile_payment()
