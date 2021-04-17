import tempfile
import shutil

from django.core.cache import caches
from django.test import Client, TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

from posts.models import Comment, Group, Post, User
from posts.settings import POSTS_QUANTITY

INDEX = reverse('index')
NEW_POST = reverse('new_post')
PROFILE = reverse('profile', args=['TestUser'])
GROUP_POSTS = reverse('group_posts', args=['test-group'])


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
        self.my_cache = caches['default']
        self.my_cache.clear()
        self.my_cache.close()

    def test_pages_shows_correct_page_context(self):
        """Шаблоны сформированы с правильным контекстом."""
        URLS = [
            INDEX,
            GROUP_POSTS,
            PROFILE,
            self.POST
        ]
        for url in URLS:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                if url == self.POST:
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

    def test_page_shows_correct_group_context(self):
        """Шаблон сформирован с правильным контекстом 'group'."""
        response = self.authorized_client.get(GROUP_POSTS)
        group = response.context['group']
        self.assertEqual(group.title, self.group.title)
        self.assertEqual(group.slug, self.group.slug)
        self.assertEqual(group.description, self.group.description)


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


class CommentViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='TestUser')
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client.force_login(self.user)

    def test_only_authorized_comment(self):
        guest_comment = Comment.objects.create(
            post=self.post,
            author=self.guest_client,
            text='NOT_AUTHORIZED'
        )
        print(guest_comment)
        authorized_comment = Comment.objects.create(
            post=self.post,
            author=self.authorized_client,
            text='AUTHORIZED')
        print(authorized_comment)


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
