from emails.base_emails import BaseEmail


class ResetPasswordEmail(BaseEmail):
    email_template_name = "emails/users/password_reset.html"

    def __init__(self, email_from, user, token):
        self.subject = "Noteneo: Reset your password"
        self.email_from = email_from
        self.user = user
        self.token = token

    def get_context_data(self):
        return {
            'user': self.user,
            'token': self.token
        }
