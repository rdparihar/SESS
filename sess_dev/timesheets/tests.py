from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import TimeRecords
import datetime

class TimeRecordsModelTests(TestCase):
    def test_get_week_returns_iso_week_number(self):
        date = datetime.date(2021, 1, 4)  # Monday of week 1
        record = TimeRecords.objects.create(emp_id=1, ts_date=date, ts_desc='Work')
        self.assertEqual(record.get_week(), date.isocalendar()[1])

class TimeEntryApproveViewTests(TestCase):
    def test_view_provides_current_week(self):
        response = self.client.get(reverse('timeEntryApprove'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['c_week'],
            timezone.now().isocalendar()[1]
        )
