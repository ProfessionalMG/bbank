from unittest import TestCase

from account.models import User


class UserModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            contact='1234567890',
        )

    def test_user_creation(self):
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')
        self.assertEqual(self.user.contact, '1234567890')
        self.assertFalse(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_verified)

    def test_str_representation(self):
        self.assertEqual(str(self.user), 'test@example.com')

    def test_required_fields(self):
        fields = User.REQUIRED_FIELDS
        self.assertIn('first_name', fields)
        self.assertIn('last_name', fields)
        self.assertIn('contact', fields)

    def test_unique_email(self):
        with self.assertRaises \
                    (Exception):  # Intentionally broad exception since the exact one might vary based on your setup.
            User.objects.create(email='test@example.com')
