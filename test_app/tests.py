from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from .models import Book, Country, Location, Student
from smart_selects.views import filterchain, filterchain_all, is_m2m


class ModelTests(TestCase):
    fixtures = ['chained_select', 'chained_m2m_select', 'grouped_select', 'user']

    def test_reverse_relationship_manager(self):
        cr = Country.objects.get(name='Czech republic')
        self.assertEqual(list(cr.location_set.all().values_list('city', flat=True)), ['Praha'])


class ViewTests(TestCase):
    fixtures = ['chained_select', 'chained_m2m_select', 'grouped_select', 'user']

    def setUp(self):
        self.factory = RequestFactory()
        self.assertTrue(self.client.login(username='admin', password='admin'))

    # chained foreignkey
    def test_location_add_get(self):
        response = self.client.get(reverse('admin:test_app_location_add'), follow=True)
        self.assertContains(response, 'Europe')
        self.assertContains(response, 'America')
        self.assertContains(response, 'var value = undefined;')

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

    def test_location_change_get(self):
        response = self.client.get(reverse('admin:test_app_location_change', args=(1,)))
        self.assertContains(response, 'Europe')
        self.assertContains(response, 'var value = 1')

    def test_filterchain_view_for_chained_foreignkey(self):
        request = self.factory.get('')
        response = filterchain(request, 'test_app', 'Country', 'continent', 'test_app', 'Location', 'country', 1)
        expected_value = '[{"value": 1, "display": "Czech republic"}, {"value": 3, "display": "Germany"}, {"value": 4, "display": "Great Britain"}]'
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), expected_value)

    def test_filterchain_all_view_for_chained_foreignkey(self):
        request = self.factory.get('')
        response = filterchain_all(request, 'test_app', 'Country', 'continent', 'test_app', 'Location', 'country', 1)
        expected_value = '[{"display": "Czech republic", "value": 1}, {"display": "Germany", "value": 3},'\
            ' {"display": "Great Britain", "value": 4}, {"display": "---------", "value": ""}, {"display": "New York", "value": 2}]'
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), expected_value)

    def test_limit_to_choice_for_chained_foreignkey(self):
        request = self.factory.get('')
        # filterchain
        response = filterchain(request, 'test_app', 'Country', 'continent', 'test_app', 'Location1', 'country', 1)
        expected_value = '[{"value": 3, "display": "Germany"}, {"value": 4, "display": "Great Britain"}]'
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), expected_value)
        # filterchain_all
        response = filterchain_all(request, 'test_app', 'Country', 'continent', 'test_app', 'Location1', 'country', 1)
        expected_value = '[{"value": 3, "display": "Germany"}, {"value": 4, "display": "Great Britain"}, {"display": "---------", "value": ""}]'
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), expected_value)

    # chained manytomany
    def test_book_add_get(self):
        response = self.client.get(reverse('admin:test_app_book_add'))
        self.assertContains(response, 'Publication 1')
        self.assertContains(response, 'var value = ""')

    def test_book_add_post(self):
        post_data = {
            'publication': '1',
            'writer': '2',
            'name': 'Book 2',
        }
        self.client.post(reverse('admin:test_app_book_add'), post_data, follow=True)
        book = Book.objects.get(writer__pk=2, publication__pk=1)
        self.assertEquals(book.name, 'Book 2')

    def test_book_add_post_no_data(self):
        post_data = {
            'publication': '1',
            'name': 'Book 2'
        }
        response = self.client.post(reverse('admin:test_app_book_add'), post_data)
        self.assertContains(response, 'This field is required.')
        self.assertContains(response, 'var value = []')

    def test_book_change_get(self):
        response = self.client.get(reverse('admin:test_app_book_change', args=(1,)), follow=True)
        self.assertContains(response, 'var value = [3];')

    def test_filterchain_view_for_chained_manytomany(self):
        request = self.factory.get('')
        response = filterchain(request, 'test_app', 'Writer', 'publications', 'test_app', 'Book', 'writer', 1)
        expected_value = '[{"display": "Author 3", "value": 3}]'
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), expected_value)

    def test_limit_to_choice_for_chained_manytomany(self):
        request = self.factory.get('')
        # filterchain
        response = filterchain(request, 'test_app', 'Writer', 'publications', 'test_app', 'Book1', 'writer', 1)
        expected_value = '[]'
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), expected_value)

    # grouped foreignkey
    def test_student_add_get(self):
        response = self.client.get(reverse('admin:test_app_student_add'))
        self.assertContains(response, '<optgroup label="Grade 1">\n<option value="1">   Team 1</option>\n</optgroup>')
        self.assertContains(response, '<optgroup label="Grade 2">\n<option value="2">   Team 2</option>\n</optgroup>')

    def test_student_add_post(self):
        post_data = {
            'name': 'Student 2',
            'grade': 2,
            'team': 2
        }
        response = self.client.post(reverse('admin:test_app_student_add'), post_data)  # noqa: F841
        student = Student.objects.get(grade=2, team=2)
        self.assertEquals(student.name, 'Student 2')

    # chained without foreign key field
    def test_view_for_chained_charfield(self):
        request = self.factory.get('')
        # filterchain
        response = filterchain(request, 'test_app', 'Tag', 'kind', 'test_app', 'TagResource', 'kind', 'music')
        expected_value = '[{"display": "reggae", "value": 2}, {"display": "rock-and-roll", "value": 1}]'
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), expected_value)

    def test_is_m2m_for_chained_charfield(self):
        try:
            from django.apps import apps
            get_model = apps.get_model
        except ImportError:
            from django.db.models.loading import get_model

        # should return false
        self.assertEquals(is_m2m(get_model('test_app', 'TagResource'), 'kind'), False)
