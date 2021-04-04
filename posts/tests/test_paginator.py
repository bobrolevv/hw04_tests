


# class PaginatorViewsTest(TestCase):
#     # Здесь создаются фикстуры: клиент и 13 тестовых записей.
#     ...
#
#     def test_first_page_containse_ten_records(self):
#         response = self.client.get(reverse('index'))
#         # Проверка: количество постов на первой странице равно 10.
#
#         self.assertEqual(len(response.context.get('page').object_list), 10)
#
#     def test_second_page_containse_three_records(self):
#         # Проверка: на второй странице должно быть три поста.
#         response = self.client.get(reverse('index') + '?page=2')
#         self.assertEqual(len(response.context.get('page').object_list), 3)

# Дополнительно можно проверить, что содержимое постов на странице
# соответствует ожиданиям — подобную проверку вы проводили, тестируя
# views. Получить содержимое страницы поможет запрос
#         response.context.get('page').object_list