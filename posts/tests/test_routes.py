from django.test import TestCase
from django.urls import reverse

from posts.models import Group, Post, User


class RoutesTest(TestCase):

    def test_routes(self):
        user = User.objects.create_user(username='TestUser')
        post = Post.objects.create(
            text='test-text-test',
            group=Group.objects.create(
                slug='test-slug'
            ),
            author=user,
        )
        URLS = [
            [reverse('index'), '/'],
            [reverse('new_post'), '/new/'],
            [reverse(
                'group_posts',
                args=[post.group.slug]
            ), f'/group/{post.group.slug}/'
            ],
            [reverse(
                'profile',
                args=[user.username]
            ), f'/{user.username}/'
            ],
            [reverse(
                'post',
                args=[post.author.username, post.id]
            ), f'/{user.username}/{post.id}/'
            ],
            [reverse(
                'post_edit',
                args=[post.author.username, post.id]
            ), f'/{user.username}/{post.id}/edit/'
            ],
        ]
        for url_name, url in URLS:
            self.assertEqual(url_name, url)
