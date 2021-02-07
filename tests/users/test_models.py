from django.conf import settings
from django.test import TestCase

from users import models as users_models


class UserModelTestCase(TestCase):
    user: users_models.User

    def setUp(self) -> None:
        self.user = users_models.User.objects.create(email='test@noteneo.test')
        self.user.set_password('2137jp2')
        self.user.save()

    def test_user_setup(self) -> None:
        self.assertEqual(self.user.email, 'test@noteneo.test')
        self.assertEqual(self.user.first_name, '')
        self.assertEqual(self.user.get_image_url(), settings.MEDIA_URL + settings.DEFAULT_PROFILE_IMAGE)
