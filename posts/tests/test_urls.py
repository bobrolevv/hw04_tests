from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from posts.models import Group

User = get_user_model()


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Group.objects.create(
            title="Тестовая группа",
            slug="test_slug",
            description="Описание",
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='Vasya')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_urls_status_code_200(self):
        """Проверка доступности страниц tested_urls любому пользователю"""
        tested_urls = ['/',
                       '/group/test_slug/',
                       '/auth/signup/',
                       ]
        for url in tested_urls:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_urls_status_code_200_authorized(self):
        """Проверка доступности страниц tested_urls авторизованному пользователю"""
        tested_urls = ['/',
                       '/group/test_slug/',
                       '/new/'
                       ]
        for url in tested_urls:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_task_list_url_redirect_anonymous_on_admin_login(self):
        """Страница по адресу /new/ перенаправит анонимного пользователя
        на страницу логина."""
        response = self.guest_client.get('/new/', follow=True)
        self.assertRedirects(
            response, '/auth/login/?next=/new/')

    def test_about_url_uses_correct_template(self):
        """Проверка шаблона для адресов из templates_url_names"""
        templates_url_names = {
            'index.html': '/',
            'new_post.html': '/new/',
            'group.html': '/group/test_slug/',
        }
        for template, reverse_name in templates_url_names.items():
            with self.subTest():
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
