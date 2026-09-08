from django.urls import path

from . import views

urlpatterns = [
    path("", views.class_list, name="class_list"),
    path("add/", views.class_add, name="class_add"),
    path("<int:pk>/", views.class_detail, name="class_detail"),
]
