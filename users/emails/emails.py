from typing import List
from emails.base_emails import EmailFactoryInterface


class WelcomeEmail(EmailFactoryInterface):
    email_template_name: str = "emails/users/welcome.html"
    subject: str = "Noteneo: Welcome"

    user = None
    email_to: List[str]

    def create_welcome_email(self, user):
        self.user = user
        self.email_to = [self.user.email]
        return self.create_email()

    def get_context_data(self):
        return {
            'user': self.user,
        }


class ResetPasswordEmail(EmailFactoryInterface):
    email_template_name: str = "emails/users/password_reset.html"
    subject: str = "Reset your password"

    user = None
    email_to: List[str]
    token: str

    def create_reset_password_email(self, user, token: str):
        self.user = user
        self.email_to = [self.user.email]
        self.token = token

        return self.create_email()

    def get_context_data(self):
        return {
            'user': self.user,
            'token': self.token
        }
