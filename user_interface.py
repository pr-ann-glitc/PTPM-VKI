from abc import ABC, abstractmethod

class AbstractUserInterface(ABC):
    @abstractmethod
    def get_input(self, prompt: str) -> str:
        ...
    @abstractmethod
    def show_result(self, message) -> None:
        ...

class UserInterface(AbstractUserInterface):
    def get_input(self, prompt: str) -> str:
        return input(prompt)
    def show_result(self, message) -> None:
        print(message)