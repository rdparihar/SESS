from django.test import TestCase, RequestFactory
from .views import lmsList
from .models import lms_details, lms_count

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


class LmsCountModelTests(TestCase):
    def test_str_returns_employee_id(self):
        count = lms_count.objects.create(emp_id=1, ls_total=10, ls_availed=2, ls_balance=8)
        self.assertEqual(str(count), '1')
