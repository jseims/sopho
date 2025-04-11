from abc import ABC, abstractmethod

class MessageDelegate(ABC):
    def __init__(self, id):
        self.id = id

    @abstractmethod
    def get_text(self):
        pass

    @abstractmethod
    def send_message(self, text):
        pass
