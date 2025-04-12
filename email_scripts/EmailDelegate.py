from MessageDelegate import MessageDelegate
import re
import textwrap
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Cc, Content, Header
from email.utils import parseaddr
import db

try:
  from localsettings import *
except:
  print("Error reading localsettings")

class EmailDelegate(MessageDelegate):

    def __init__(self, msg_id):
        self.msg_id = msg_id
        # load the email from db
        emails = list(db.query("""SELECT * from email WHERE id = %s""", [self.msg_id]))
        if emails:
            self.email = emails[0]
            self.to_list = self._cleanup_to(self.email['email_to'])
            self.cc_list = self._cleanup_to(self.email['email_cc'])
        else:
           print("WARNING: no email found with id %s" % (self.msg_id))


    # remove all @sopho.ai emails to prevent loops and merge to and cc into a single string
    def _cleanup_to(self, email_list):
        # Split on commas and strip whitespace
        raw_addresses = [addr.strip() for addr in email_list.split(',') if addr.strip()]

        # Extract actual email addresses using regex
        email_regex = re.compile(r'[\w\.-]+@[\w\.-]+')
        filtered = []

        print("raw addr")
        print(raw_addresses)

        for entry in raw_addresses:
            match = email_regex.search(entry)
            if match:
                email = match.group(0)
                if not email.lower().endswith("@sopho.ai"):
                    filtered.append(email)
                else:
                    self.sopho_email = email

        return filtered

    # clean it up for sending to LLM
    def get_conversation_text(self, context_window):
        response = "From: " + self.email['email_from'] + "\n"
        response += "To: " + (", ").join(self.to_list) + "\n"
        response += "CC: " + (", ").join(self.cc_list) + "\n"
        response += "Subject: " + self.email['subject'] + "\n\n"
        response += self.email['email_text']

        # conservatively, we allow 2 chars per token in size to stay well within context window length
        max_length = context_window * 2
        response = response[:max_length]
        return response

    def _compute_from_label(self):
        # Extract just the email part from name/email string
        _, email = parseaddr(self.sopho_email)

        # Split at @ and return the local part
        self.from_label = email.split('@')[0] if '@' in email else ''


    # return the llm_config that should serve this email
    def get_llm_config(self):
        self._compute_from_label()
        print("from_label %s" % (self.from_label))
        llms = list(db.query("""SELECT * from llm_config WHERE email = %s""", [self.from_label]))
        if llms:
            return llms[0]
        else:
            print("ERROR: no llm_config found for email %s" % (self.from_label))

    def _format_quoted_message(self, from_field, date_field, body):
        # Format the header line
        header_line = f"On {date_field}, {from_field} wrote:"

        # Add '> ' before every line of the original message
        quoted_lines = [f"> {line}" for line in body.strip().splitlines()]
        quoted_body = "\n".join(quoted_lines)

        return f"{header_line}\n{quoted_body}"

    def _subject_to_reply(self, subject):
        # Remove all existing "Re:" (case-insensitive, repeated, with optional whitespace)
        subject = "Re: " + subject
        clean = re.sub(r'^(Re:\s*)+', '', subject, flags=re.IGNORECASE)
        return f"Re: {clean.strip()}"


    def send_message(self, new_message):
        # Extract data from original message
        from_email = self.from_label + '@sopho.ai'  # your sending address
        subject = self.email.get('subject', '')
        message_id = self.email.get('message_id')
        in_reply_to = self.email.get('in_reply_to') or message_id
        references = self.email.get('email_references') or message_id
        date = self.email.get('date', '')
        original_text = self.email.get('email_text', '')
            
        # Format the reply body
        quoted = self._format_quoted_message(from_email, date, original_text)
        reply_body = f"{new_message}\n\n{quoted}"

        subject = self._subject_to_reply(subject)

        # make sure the original sender gets a copy
        self.to_list.append(self.email['email_from'])

        # Send via SendGrid
        mail = Mail(
            from_email=Email(from_email),
            to_emails=[To(addr) for addr in self.to_list],
            subject=subject,
            plain_text_content=Content("text/plain", reply_body)
        )

        # Add CC after construction
        mail.cc = [Cc(addr) for addr in self.cc_list]

        print(self.to_list)
        print("CC emails:")
        print([Cc(addr) for addr in self.cc_list])
        print(self.cc_list)

        mail.header = [
            Header("In-Reply-To", in_reply_to, p=0),
            Header('References', references, p=0)
        ]

        sg = SendGridAPIClient(api_key=SENDGRID_API_KEY)
        response = sg.send(mail)
        print("Status Code:", response.status_code)
