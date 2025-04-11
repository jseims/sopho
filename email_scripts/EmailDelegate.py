from MessageDelegate import MessageDelegate

class EmailDelegate(MessageDelegate):
    def get_text(self):
        return "This is an email message."

    def send_message(self, text):
        print(f"Sending email to {self.id}: {text}")
