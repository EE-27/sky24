from school.apps import SchoolConfig
from rest_framework.routers import DefaultRouter

from school.views import CourseViewSet

app_name = SchoolConfig.name

router = DefaultRouter()  # pro ViewSet stačí takto
router.register(r"courses", CourseViewSet, basename="courses")
urlpatterns = [

] + router.urls