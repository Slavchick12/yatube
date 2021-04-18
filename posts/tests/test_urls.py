from django.test import TestCase, Client
from django.urls import reverse

from posts.models import Group, User, Post

INDEX = reverse('index')
NEW_POST = reverse('new_post')
GROUP_POSTS = reverse('group_posts', args=['test-group'])
PROFILE = reverse('profile', args=['TestUser'])
LOGIN = reverse('login')


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='test_title',
            slug='test-group',
            description='test_description',
        )
        cls.user = User.objects.create_user(username='TestUser')
        cls.non_author = User.objects.create_user(username='TestUser2')
        cls.post = Post.objects.create(
            text='Текст-тест',
            author=cls.user,
            group=cls.group,
        )
        cls.POST = reverse(
            'post',
            args=[cls.user.username, cls.post.id]
        )
        cls.POST_EDIT = reverse(
            'post_edit',
            args=[cls.user.username, cls.post.id]
        )
        cls.COMMENT = reverse(
            'add_comment',
            args=[cls.user.username, cls.post.id]
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.authorized_client2 = Client()   # не автор поста
        self.authorized_client2.force_login(self.non_author)

    def test_urls_guest(self):
        """Страницы доступны пользователям."""
        urls = [
            [self.guest_client, INDEX, 200],
            [self.guest_client, GROUP_POSTS, 200],
            [self.guest_client, self.POST, 200],
            [self.authorized_client, NEW_POST, 200],
            [self.authorized_client, self.POST_EDIT, 200],
            [self.authorized_client, self.COMMENT, 200],
            [self.guest_client, NEW_POST, 302],
            [self.guest_client, self.POST_EDIT, 302],
            [self.authorized_client2, self.POST_EDIT, 302],
            [self.guest_client, self.COMMENT, 302],
            [self.guest_client, '404', 404],
            [self.guest_client, 'group_posts/404', 404],
        ]
        for client, url_name, status in urls:
            with self.subTest(url=url_name):
                self.assertEqual(client.get(url_name).status_code, status)

    def test_urls_redirect_users(self):
        """Страницы правильно перенаправляют пользователей."""
        URL_LOGIN = LOGIN + '?next='
        urls = [
            [NEW_POST, self.guest_client, URL_LOGIN + NEW_POST],
            [
                self.POST_EDIT, self.guest_client,
                URL_LOGIN + self.POST_EDIT
            ],
            [
                self.POST_EDIT, self.authorized_client2,
                self.POST
            ]
        ]
        for url_name, client, url in urls:
            with self.subTest(url=url):
                self.assertRedirects(
                    client.get(
                        url_name, follow=True
                    ), url
                )

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            INDEX: 'index.html',
            GROUP_POSTS: 'group.html',
            NEW_POST: 'new.html',
            self.POST: 'post.html',
            self.POST_EDIT: 'new.html',
            PROFILE: 'profile.html',
        }

        for reverse_name, template in templates_url_names.items():
            with self.subTest(url=reverse_name):
                self.assertTemplateUsed(
                    self.authorized_client.get(reverse_name), template
                )
