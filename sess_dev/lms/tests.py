from django.test import TestCase, RequestFactory
from .views import lmsList
from .models import lms_details

class LmsListViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_year_is_all_when_query_zero(self):
        request = self.factory.get('/lms/', {'q': '0'})
        request.session = {'emp_id': 1}
        view = lmsList()
        view.request = request
        view.object_list = lms_details.objects.none()
        context = view.get_context_data()
        self.assertEqual(context.get('year'), 'All')
