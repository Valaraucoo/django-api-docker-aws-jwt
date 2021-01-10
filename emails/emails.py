from typing import List

from emails.base_emails import EmailFactoryInterface


class ResetPasswordEmail(EmailFactoryInterface):
    email_template_name: str = "emails/users/password_reset.html"
    subject: str = "Noteneo: Reset your password"

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
