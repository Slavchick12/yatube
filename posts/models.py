from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    text = models.TextField('текст', help_text='Здесь Ваш текст')
    pub_date = models.DateTimeField(
        'дата публикации', auto_now_add=True, db_index=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts',
        verbose_name='автор',
    )
    group = models.ForeignKey(
        'Group', on_delete=models.SET_NULL,
        related_name='posts', blank=True, null=True, verbose_name='группы',
        help_text='Можете выбрать группу'
    )
    image = models.ImageField(upload_to='posts/', blank=True, null=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name_plural = 'Посты'
        verbose_name = 'пост'

    def __str__(self):
        return self.text[:15]


class Group(models.Model):
    title = models.CharField(
        'название группы', max_length=200,
        help_text='Придумайте название группы')
    slug = models.SlugField(
        'ключ для построения урла', unique=True,
        help_text=('Укажите ключ для страницы задачи. '
                   'Используйте только латиницу, цифры, дефисы '
                   'и знаки подчёркивания'))
    description = models.TextField(
        'описание', help_text='Дайте описание группе')

    class Meta:
        verbose_name_plural = 'Группы'
        verbose_name = 'группу'

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments',
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',
        verbose_name='автор',
    )
    text = models.TextField('текст', help_text='Здесь Ваш текст')
    created = models.DateTimeField(
        'дата публикации', auto_now_add=True,
    )


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower',
        verbose_name='подписчик',
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following',
        verbose_name='автор',
    )
