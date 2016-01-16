from django.core.urlresolvers import reverse
from django.test import TestCase
from .models import Country
  
class ViewTests(TestCase):
    fixtures = [ 'data', ]

    def setUp(self):
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
        response = self.client.post(reverse('admin:test_app_location_add'), post_data, follow=True)
        country = Country.objects.get(pk=2)
        location = country.location_set.first()
        self.assertEquals(location.city, 'New York')
        self.assertEquals(location.street, 'Wallstreet')

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
