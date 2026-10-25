from abc import ABC, abstractmethod


class AbstractExternalService(ABC):
    @abstractmethod
    def send(self, message: str) -> bool:
        ...


class FakeEmailService(AbstractExternalService):
    def __init__(self):
        self.sent_messages: list[str] = []

    def send(self, message: str) -> bool:
        self.sent_messages.append(message)
        return True