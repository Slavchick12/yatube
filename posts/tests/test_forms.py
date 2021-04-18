import shutil
import tempfile

from django.test import Client, TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

from posts.forms import PostForm
from posts.models import Group, Post, User
from django import forms


INDEX = reverse('index')
NEW_POST = reverse('new_post')
LOGIN = reverse('login')


class PostFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        cls.form = PostForm()
        cls.group = Group.objects.create(
            title='test_title',
            slug='test-group',
            description='test_description',
        )
        cls.group_2 = Group.objects.create(
            title='test_title_2',
            slug='test-group-2',
            description='test_description_2',
        )
        cls.author = User.objects.create_user(username='TestUser1')
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.author,
            group=cls.group
        )
        cls.POST = reverse(
            'post',
            args=[cls.author.username, cls.post.id]
        )
        cls.POST_EDIT = reverse(
            'post_edit',
            args=[cls.author.username, cls.post.id]
        )
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

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)

    def test_new_post_reverse(self):
        """ Проверка на появление нового поста """
        post_count = Post.objects.count()
        posts_id = set(Post.objects.all().values_list('id', flat=True))
        form_data = {
            'text': 'TestText',
            'group': self.group_2.id,
            'image': self.image
        }
        response_guest = self.guest_client.post(
            NEW_POST,
            data=form_data,
            follow=True,
        )
        response = self.authorized_client.post(
            NEW_POST,
            data=form_data,
            follow=True,
        )
        self.assertRedirects(response, INDEX)
        self.assertEqual(Post.objects.count(), post_count + 1)
        posts_id_updated = set(Post.objects.all().values_list('id', flat=True))
        set_id = posts_id_updated.difference(posts_id)
        if set_id != {}:
            for id in set_id:
                new_post = Post.objects.get(id=id)
                self.assertEqual(form_data['text'], new_post.text)
                self.assertEqual(form_data['group'], new_post.group.id)
                self.assertEqual(form_data['image'], self.image)
                self.assertEqual(self.author, new_post.author)
        self.assertEqual(len(set_id), 1)
        self.assertRedirects(response_guest, LOGIN + '?next=' + NEW_POST)

    def test_post_edit(self):
        """ Проверка на изменение поста """
        post_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст (edit)',
            'group': self.group_2.id,
        }
        response_guest = self.guest_client.post(
            self.POST_EDIT,
            data=form_data,
            follow=True,
        )
        response = self.authorized_client.post(
            self.POST_EDIT,
            data=form_data,
            follow=True,
        )
        self.assertRedirects(response_guest, LOGIN + '?next=' + self.POST_EDIT)
        self.assertRedirects(response, self.POST)
        self.assertEqual(Post.objects.count(), post_count)
        post_edit = response.context['post']
        self.assertEqual(form_data['text'], post_edit.text)
        self.assertEqual(form_data['group'], post_edit.group.id)
        self.assertEqual(self.post.author, post_edit.author)

    def test_pages_shows_correct_context(self):
        """Шаблоны сформированы с правильным контекстом."""
        URLS = [NEW_POST, self.POST_EDIT]
        for url in URLS:
            response = self.authorized_client.get(url)
            form_fields = {
                'text': forms.fields.CharField,
                'group': forms.fields.ChoiceField,
                'image': forms.ImageField
            }
            for value, expected in form_fields.items():
                with self.subTest(value=value):
                    form_field = response.context['form'].fields[value]
                    self.assertIsInstance(form_field, expected)
