from django.test import Client, TestCase
from django.urls import reverse

from posts.models import User


class PattertnsTest(TestCase):

    def setUp(self):
        self.authorized_client = Client()
        self.user = User.objects.create_user(username='TestUser')
        self.authorized_client.force_login(self.user)

    def test_added_page_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            'about/author.html': reverse('about:author'),
            'about/tech.html': reverse('about:tech'),
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
