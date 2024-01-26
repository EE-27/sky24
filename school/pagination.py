from rest_framework.pagination import PageNumberPagination


class CoursePagination(PageNumberPagination):
    page_size = 5


class LessonPagination(PageNumberPagination):
    page_size = 10
