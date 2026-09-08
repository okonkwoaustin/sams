from django.urls import path

from . import views

urlpatterns = [
    path("history/", views.attendance_history, name="attendance_history"),
    path("take/<int:class_id>/", views.attendance_take, name="attendance_take"),
    path("<int:pk>/", views.attendance_detail, name="attendance_detail"),
]
