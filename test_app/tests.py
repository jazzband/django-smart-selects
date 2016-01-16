from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from .models import Book, Location
from smart_selects.views import filterchain, filterchain_all


class ViewTests(TestCase):
    fixtures = ['data', ]

    def setUp(self):
        self.factory = RequestFactory()
        self.assertTrue(self.client.login(username='admin', password='admin'))

    def test_location_add_get(self):
        response = self.client.get(reverse('admin:test_app_location_add'), follow=True)
        self.assertContains(response, 'Europe')
        self.assertContains(response, 'America')

    def test_location_add_post(self):
        post_data = {
            'continent': '1',
            'country': '2',
            'city': 'New York',
            'street': 'Wallstreet',
        }
        self.client.post(reverse('admin:test_app_location_add'), post_data, follow=True)
        location = Location.objects.get(country__pk=2, continent__pk=1)
        self.assertEquals(location.city, 'New York')
        self.assertEquals(location.street, 'Wallstreet')

    def test_book_add_get(self):
        response = self.client.get(reverse('admin:test_app_book_change', args=(1,)), follow=True)
        self.assertContains(response, 'var value = [3];')

    def test_book_add_post(self):
        post_data = {
            'publication': '1',
            'writer': '2',
            'name': 'Book 2',
        }
        self.client.post(reverse('admin:test_app_book_add'), post_data, follow=True)
        book = Book.objects.get(writer__pk=2, publication__pk=1)
        self.assertEquals(book.name, 'Book 2')

    def test_location_add_post_no_data(self):
        post_data = {
            'continent': '1',
            'country': '',
            'city': 'New York',
            'street': 'Wallstreet',
        }
        response = self.client.post(reverse('admin:test_app_location_add'), post_data)
        self.assertContains(response, 'This field is required.')
        self.assertContains(response, 'var value = undefined;')

    def test_filterchain_view(self):
        request = self.factory.get('')
        response = filterchain(request, 'test_app', 'Country', 'continent', 'test_app', 'Location', 'country', 1)
        expected_value = '[{"value": 1, "display": "Czech republic"}, {"value": 3, "display": "Germany"}, {"value": 4, "display": "Great Britain"}]'
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), expected_value)

    def test_filterchain_all_view(self):
        request = self.factory.get('')
        response = filterchain_all(request, 'test_app', 'Country', 'continent', 'test_app', 'Location', 'country', 1)
        expected_value = '[{"display": "Czech republic", "value": 1}, {"display": "Germany", "value": 3},'\
            ' {"display": "Great Britain", "value": 4}, {"display": "---------", "value": ""}, {"display": "New York", "value": 2}]'
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), expected_value)
