from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='index_page'),
    path('login/',views.user_login,name='login_page'),
    path('signup/',views.register,name='signup_page'),
    path('tasks/create', views.create_task, name='create_task'),
    path('tasks/', views.list_tasks, name='tasks'),
    path('tasks/done/<int:task_id>', views.mark_task_done, name='mark_task_done'),
    path('tasks/abort/<int:task_id>', views.abort_task, name='abort_task'),
]