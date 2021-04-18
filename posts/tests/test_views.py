import tempfile
import shutil

from django.core.cache import caches
from django.test import Client, TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

from posts.models import Follow, Group, Post, User
from posts.settings import POSTS_QUANTITY

INDEX = reverse('index')
NEW_POST = reverse('new_post')
PROFILE = reverse('profile', args=['TestUser'])
GROUP_POSTS = reverse('group_posts', args=['test-group'])
FOLLOW_INDEX = reverse('follow_index')
PROFILE_FOLLOW = reverse('profile_follow', args=['TestUser'])
PROFILE_UNFOLLOW = reverse('profile_unfollow', args=['TestUser'])


class ContextsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        cls.group = Group.objects.create(
            title='test_title',
            slug='test-group',
            description='test_description',
        )
        cls.user = User.objects.create_user(username='TestUser')
        cls.follower = User.objects.create(username='TestUser2')
        cls.unfollower = User.objects.create(username='TestUser3')
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.image = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
            group=cls.group,
            image=cls.image
        )
        cls.POST = reverse(
            'post',
            args=[cls.user.username, cls.post.id]
        )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.authorized_client_follower = Client()
        self.authorized_client_follower.force_login(self.follower)
        self.authorized_client_unfollower = Client()
        self.authorized_client_unfollower.force_login(self.unfollower)
        self.my_cache = caches['default']
        self.my_cache.clear()
        self.my_cache.close()

    def test_pages_shows_correct_page_context(self):
        """Шаблоны сформированы с правильным контекстом."""
        URLS = [
            [INDEX, 'page'],
            [GROUP_POSTS, 'page'],
            [PROFILE, 'page'],
            [self.POST, 'post'],
        ]
        for url, context in URLS:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                if context == 'post':
                    post = response.context['post']
                else:
                    self.assertEqual(
                        len(response.context['page'].object_list), 1
                    )
                    post = response.context['page'][0]
                self.assertEqual(post.group, self.post.group)
                self.assertEqual(post.text, self.post.text)
                self.assertEqual(post.author, self.post.author)
                self.assertEqual(post.image, self.post.image)

    def test_pages_shows_correct_author_context(self):
        """Шаблоны сформированы с правильным контекстом 'aurhor'."""
        URLS = [self.POST, PROFILE]
        for url in URLS:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(
                    response.context['author'].username, self.user.username
                )

    def test_new_post_in_follow_index(self):
        """ Новая запись пользователя появляется и не появляется в ленте """
        self.authorized_client_follower.get(PROFILE_FOLLOW)
        new_post = self.authorized_client.post(
            reverse('new_post'),
            {'text': 'Тест подписки'},
            follow=True
        )
        response = self.authorized_client_follower.get(FOLLOW_INDEX)
        response_unfollower = self.authorized_client_unfollower.get(
            FOLLOW_INDEX)
        self.assertIn(new_post.context['page'][0], response.context['page'])
        self.assertNotIn(
            new_post.context['page'][0],
            response_unfollower.context['page']
        )

    def test_new_follow_(self):
        """ Проверка подписки и отписки """
        count_before_follow = Follow.objects.count()
        self.authorized_client_follower.get(PROFILE_FOLLOW)
        self.assertEqual(Follow.objects.count(), count_before_follow + 1)
        count_later_follow = Follow.objects.count()
        self.authorized_client_follower.get(PROFILE_UNFOLLOW)
        self.assertEqual(Follow.objects.count(), count_later_follow - 1)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        test_user = User.objects.create_user(username='TestUser')
        cls.group = Group.objects.create(
            title='test_title',
            slug='test-group',
            description='test_description',
        )
        posts = (Post(text='Тестовый текст %s' % i,
                 author=test_user,
                 group=cls.group) for i in range(POSTS_QUANTITY + 12))
        cls.test_posts = Post.objects.bulk_create(posts)

    def setUp(self):
        self.guest_client = Client()

    def test_first_page_quantiny_records(self):
        URLS = [INDEX, GROUP_POSTS, PROFILE]
        for url in URLS:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertLess(
                    len(response.context.get('page').object_list),
                    POSTS_QUANTITY + 1)

    def test_second_page_quantiny_records(self):
        URLS = [INDEX, GROUP_POSTS, PROFILE]
        for url in URLS:
            with self.subTest(url=url):
                response = self.client.get(url + '?page=2')
                self.assertLess(
                    len(response.context.get('page').object_list),
                    POSTS_QUANTITY + 1)


class CachesTest(TestCase):

    def setUp(self):
        self.guest_client = Client()

    def test_index_cache_instantly(self):
        response_before = self.guest_client.get(INDEX)
        Post.objects.create(
            text='Тестовый текст',
            author=User.objects.create_user(username='TestUser'),
        )
        response_after = self.guest_client.get(INDEX)
        self.assertEqual(
            response_before.content,
            response_after.content
        )
