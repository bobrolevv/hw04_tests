from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from posts.models import Group, Post

User = get_user_model()


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Vasya')
        cls.user2 = User.objects.create_user(username='Vova')
        cls.group = Group.objects.create(
            title="Тестовая группа",
            slug="test_slug",
            description="Описание",
        )
        cls.post = Post.objects.create(
            text='test text',
            group=cls.group,
            author=cls.user
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.authorized_client2 = Client()
        self.authorized_client2.force_login(self.user2)
        # self.post = Post.objects.create(
        #     text='test text',
        #     # group=self.group,
        #     author=self.user)

    def test_urls_status_code_200(self):
        """Проверка доступности страниц tested_urls любому пользователю"""
        tested_urls = ['/',
                       '/group/test_slug/',
                       '/auth/signup/',
                       '/Vasya/',
                       '/Vasya/1/',
                       ]
        for url in tested_urls:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, 200, url)

    def test_urls_status_code_200_authorized(self):
        """
        1. Проверка доступности страниц tested_urls
        авторизованному пользователю
        2. Проверка доступности страницы редактирования не автору поста
        """
        # 1
        tested_urls = ['/',
                       '/group/test_slug/',
                       '/new/',
                       '/Vasya/',
                       '/Vasya/1/edit/',
                       ]
        for url in tested_urls:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, 200, url)
        # 2
        response = self.authorized_client2.get('/Vasya/1/edit/')
        self.assertEqual(response.status_code, 302,)

    def test_task_list_url_redirect_anonymous_on_admin_login(self):
        """
        1. Страница по адресу /new/ перенаправит анонимного пользователя
        на страницу логина.
        2. Проверка, правильно ли работает редирект со страницы
        /<username>/<post_id>/edit/для тех,
         у кого нет прав доступа к этой странице.
        """
        # 1
        response = self.guest_client.get('/new/', follow=True)
        self.assertRedirects(
            response, '/auth/login/?next=/new/')
        # 2
        response = self.authorized_client2.get('/Vasya/1/edit/',
                                               follow=True)
        self.assertRedirects(
            response, '/Vasya/')

    def test_about_url_uses_correct_template(self):
        """Проверка шаблона для адресов из templates_url_names"""
        templates_url_names = {
            'index.html': '/',
            'new_post.html': '/new/',
            'group.html': '/group/test_slug/',
            # 'new_post.html': '/Vasya/1/edit/',
        }
        for template, reverse_name in templates_url_names.items():
            with self.subTest():
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
