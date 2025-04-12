from abc import ABC, abstractmethod

class MessageDelegate(ABC):
    def __init__(self, msg_id):
        self.msg_id = msg_id

    @abstractmethod
    def get_conversation_text(self, context_window):
        pass

    @abstractmethod
    def get_llm_config(self):
        pass

    @abstractmethod
    def send_message(self, new_message):
        pass
