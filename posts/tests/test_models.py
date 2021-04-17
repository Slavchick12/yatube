from django.test import TestCase

from posts.models import Comment, Follow, Group, Post, User


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=User.objects.create_user(username='TestUser'),
            group=Group.objects.create(),
        )

    def test_text_label_post(self):
        field_verboses = {
            'text': 'текст',
            'pub_date': 'дата публикации',
            'author': 'автор',
            'group': 'группы',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    Post._meta.get_field(value).verbose_name, expected)

    def test_help_text_post(self):
        field_help_texts = {
            'text': 'Здесь Ваш текст',
            'group': 'Можете выбрать группу',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    Post._meta.get_field(value).help_text, expected)

    def test_post_is_text_field(self):
        post = self.post
        expected_object_name = post.text[:15]
        self.assertEquals(expected_object_name, str(post))


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='test_title',
            slug='test-group',
            description='test_description',
        )

    def test_text_label_group(self):
        field_verboses = {
            'title': 'название группы',
            'slug': 'ключ для построения урла',
            'description': 'описание',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    Group._meta.get_field(value).verbose_name, expected)

    def test_help_text_group(self):
        field_help_texts = {
            'title': 'Придумайте название группы',
            'slug': ('Укажите ключ для страницы задачи. '
                     'Используйте только латиницу, цифры, дефисы '
                     'и знаки подчёркивания'),
            'description': 'Дайте описание группе',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    Group._meta.get_field(value).help_text, expected)

    def test_group_is_text_field(self):
        expected_object_name = self.group.title
        self.assertEquals(expected_object_name, str(self.group))


class CommentModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='TestUser')
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
        )
        cls.comment = Comment.objects.create(
            post=cls.post,
            author=cls.user,
            text='test_text'
        )

    def test_text_label_comment(self):
        field_verboses = {
            'text': 'текст',
            'created': 'дата публикации'
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    Comment._meta.get_field(value).verbose_name, expected)


class FollowModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='TestUser')
        cls.user2 = User.objects.create_user(username='TestUser2')
        cls.follow = Follow.objects.create(
            user=cls.user,
            author=cls.user2
        )

    def test_text_label_follow(self):
        field_verboses = {
            'user': 'подписчик',
            'author': 'автор'
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    Follow._meta.get_field(value).verbose_name, expected)
