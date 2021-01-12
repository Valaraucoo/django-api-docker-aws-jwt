from typing import List

from django.urls import reverse

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
        reset_link = "{}?token={}".format(reverse('password_reset:reset-password-request'), self.token)
        return {
            'user': self.user,
            'reset_link': reset_link
        }
