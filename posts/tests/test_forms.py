from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post, Group, User


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='test text',
            description='Тестовый текст',
            slug='test_group'
        )
        cls.post = Post.objects.create(
            text='test text',
            group=cls.group,
            author=User.objects.create(username='asya'),
        )

    def setUp(self):
        self.user = User.objects.create_user(username='Vasya')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_post_create_in_db(self):
        post_count = Post.objects.count()
        print(f'========={post_count}========')
        form_data = {
            'text': 'Текст из формы',
            'group': self.group,
        }
        print(f'======={form_data}=====')
        self.authorized_client.post(
            reverse('posts:new_post'),
            data=form_data,
            follow=True,
        )
        self.assertEqual(Post.objects.count(), post_count + 1)
