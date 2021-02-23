class State:
    """
    Состояние описывает общий интерфейс для всех конкретных состояний.
    """

    context: "Context"

    def handle_request(self):
        raise NotImplementedError

    def set_context(self, context: "Context"):
        self.context = context


class Context:
    """
    Контекст хранит ссылку на объект состояния и делегирует ему часть работы, зависящей от состояний.
    Контекст работает с этим объектом через общий интерфейс состояний.
    Контекст должен иметь метод для присваивания ему нового объекта-состояния.
    """

    state: State

    def __init__(self, initial_state: State):
        self.change_state(initial_state)

    def change_state(self, new_state: State):
        self.state = new_state
        new_state.set_context(self)

    def run(self):
        self.state.handle_request()
