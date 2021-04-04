from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post, Group, User

User = get_user_model()


class PostsPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.create_user(username='Anton')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

        cls.group = Group.objects.create(
            title='Название Группы',
            slug='test_slug',
            description='Описание',
        )

        cls.post = Post.objects.create(
            text='Тестовый текст',
            group=cls.group,
            author=cls.user,
        )

    def test_pages_use_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_page_names = {
            'index.html': reverse('posts:index'),
            'new_post.html': reverse('posts:new_post'),
            'group.html': (
                reverse('posts:group', kwargs={'slug': 'test_slug'})
            ),
        }
        for template, reverse_name in templates_page_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_new_post_page_shows_correct_context(self):
        """Шаблон <new_post> сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:new_post'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_group_page_shows_correct_context(self):
        """Шаблон <group> сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:group', kwargs={'slug': 'test_slug'}))
        first_object = response.context['group']
        task_title_0 = first_object.title
        task_slug_0 = first_object.slug
        task_description_0 = first_object.description
        self.assertEqual(task_title_0, 'Название Группы')
        self.assertEqual(task_slug_0, 'test_slug')
        self.assertEqual(task_description_0, 'Описание')

    def test_index_page_shows_correct_context(self):
        """Шаблон <index> сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:index'))
        first_object = response.context['posts1'][0]
        task_text_0 = first_object.text
        task_group_0 = first_object.group
        task_author_0 = first_object.author
        self.assertEqual(task_text_0, 'Тестовый текст')
        self.assertEqual(task_group_0, self.group)
        self.assertEqual(task_author_0, self.user)
