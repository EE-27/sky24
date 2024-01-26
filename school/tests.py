from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from school.models import Course, Lesson, Subscription
from users.models import User


# pip3 install coverage
# coverage run --source='.' manage.py test
# coverage report

class CourseTestCase(APITestCase):

    def setUp(self) -> None:
        pass

    def test_create_course(self):

        data = {
            "title": "test",
            "description" : "test"
        }

        response = self.client.post(
            "/courses/",
            data=data
        )
        # print(response.json())
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {'id': 1, 'lesson_count': 0, 'lesson': [], 'is_subscribed': False, 'title': 'test', 'preview': None,
             'description': 'test', 'owner': None}
        )

        self.assertTrue(
            Course.objects.all().exists()
        )

    def test_list_course(self):
        Course.objects.create(
            title="list test",
            description="list test"
        )

        response = self.client.get(
            "/courses/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            [{'id': 2, 'lesson_count': 0, 'lesson': [], 'is_subscribed': False, 'title': 'list test', 'preview': None,
             'description': 'list test', 'owner': None}]
        )

class LessonCRUDTests(TestCase):
    def setUp(self):

        # Create a course
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Course Description'
        )
        # Create a lesson
        self.lesson = Lesson.objects.create(
            title='Test Lesson',
            description='Test Lesson Content',
            course=self.course
        )

    def test_create_lesson(self):
        data = {'title': 'New Lesson', 'description': 'New Lesson Content', 'course': self.course.id}
        response = self.client.post('/lesson/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_retrieve_lesson(self):
        response = self.client.get(f'/lesson/{self.lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Lesson')

    def test_update_lesson(self):
        data = {'title': 'Updated Lesson', 'description': 'Updated Lesson Content'}
        response = self.client.patch(f'/lesson/update/{self.lesson.id}/', data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lesson.objects.get(id=self.lesson.id).title, 'Updated Lesson')

    def test_delete_lesson(self):
        response = self.client.delete(f'/lesson/delete/{self.lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

class SubscriptionTests(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create(
            email='test@example.com',
            password='testpassword'
        )
        # Create a course
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Course Description'
        )
        # Create an APIClient and authenticate the user
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_subscribe_to_course(self):
        response = self.client.post(f'/subscribe/{self.course.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscription.objects.count(), 1)

    def test_unsubscribe_from_course(self):
        # Subscribe the user to the course first
        Subscription.objects.create(user=self.user, course=self.course)
        response = self.client.post(f'/unsubscribe/{self.course.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscription.objects.count(), 0)