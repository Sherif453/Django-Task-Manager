from django.urls import path
from . import web_views

urlpatterns = [
    path("", web_views.home, name="home"),
    path("register/", web_views.register_page, name="register_page"),

    path("tasks/", web_views.tasks_list, name="tasks_web_list"),
    path("tasks/new/", web_views.task_create, name="task_create"),
    path("tasks/<int:pk>/edit/", web_views.task_update, name="task_update"),
    path("tasks/<int:pk>/delete/", web_views.task_delete, name="task_delete"),
    path("tasks/<int:pk>/toggle/", web_views.task_toggle_complete, name="task_toggle"),
]
    