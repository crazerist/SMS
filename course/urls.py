from django.urls import path
from course.views import *
from course.cbvs import ScoreUpdateView


urlpatterns = [
    path('<slug:kind>/', home, name="course"),
    path('<slug:kind>/', home, name="course"),
    path('teacher/create_course', create_course, name="create_course"),
    path('teacher/view_detail/<int:course_id>', view_detail, name="view_detail"),
    path('teacher/create_schedule/<int:course_id>', create_schedule, name="create_schedule"),
    path('teacher/delete_schedule/<int:schedule_id>', delete_schedule, name="delete_schedule"),
    path('teacher/score/<int:pk>', ScoreUpdateView.as_view(), name="score"),
    path('teacher/handle_course/<int:course_id>/<int:handle_kind>', handle_course, name="handle_course"),
]
