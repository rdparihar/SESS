from django.test import TestCase

from .models import Student, University


class ModelStrTests(TestCase):
    def test_university_str(self):
        university = University.objects.create(name="Test University")
        self.assertEqual(str(university), "Test University")

    def test_student_str(self):
        university = University.objects.create(name="Test University")
        student = Student.objects.create(
            first_name="John", last_name="Doe", university=university
        )
        self.assertEqual(str(student), "John Doe")

