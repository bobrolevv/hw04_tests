from django.contrib.auth import get_user_model
from django.db import models
from pytils.translit import slugify

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        'Заголовок',
        max_length=200,
        help_text='Дайте короткое название группе',
    )
    slug = models.SlugField(
        'Слаг',
        max_length=20,
        unique=True,
        help_text=('Укажите адрес для страницы группы. Используйте только '
                   'латиницу, цифры, дефисы и знаки подчёркивания'),
    )

    description = models.TextField(
        'Описание',
        help_text='Опишите группу',
    )

    def __str__(self):
        return f'{self.title}'


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:100]
        super().save(*args, **kwargs)


class Post(models.Model):
    # objects = None
    text = models.TextField(
        'Текст',
        help_text='Опишите новость',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='posts',
    )
    group = models.ForeignKey(
        Group,
        verbose_name='Группа',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts',
        help_text = 'Выберите группу'
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:15]
