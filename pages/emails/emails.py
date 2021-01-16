from typing import Any, Dict, List

from django.core import mail

from emails import base_emails
from users import models as users_models
from pages import models as pages_models


class PagePublishedMailFactory(base_emails.EmailFactoryInterface):
    user: users_models.User
    page: pages_models.Page
    email_to: List[str]

    subject: str = "Pagex: Page created"
    email_template_name: str = "emails/pages/page-created.html"

    def create_page_published_email(self, user: users_models.User, page: pages_models.Page) -> mail.EmailMessage:
        self.user = user
        self.page = page
        self.email_to = [self.user.email] + self.email_to

        return self.create_email()

    def get_context_data(self, *args, **kwargs) -> Dict[Any, Any]:
        return {
            'user': self.user,
            'page': self.page
        }
