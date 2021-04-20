from django.test import Client, TestCase


class PostURLTests(TestCase):
    """Проверка URL адресов."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.urls = [
            'author/',
            'tech/',
        ]
        cls.template_names = [
            'about/author.html',
            'about/tech.html',
        ]

    def test_url_statik_page_guest_user(self):
        """Страницы доступны любому пользователю."""
        for url_name in self.urls:
            with self.subTest():
                response = self.guest_client.get('')
                self.assertEqual(response.status_code, 200)
