from django.urls import path
from django.views.generic.edit import CreateView
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from bboard.models import Bb
from rest_framework.routers import DefaultRouter
from bboard.views import (index, by_rubric, BbCreateView,
                          add_and_save, bb_detail, BbRubricBbsView,
                          BbDetailView, BbEditView, BbDeleteView,
                          BbRedirectView, edit, rubrics, bbs, search)

from django.contrib import admin
from .models import User

from django.urls import path
from .views import task_list, task_detail

from django.urls import path
from .views import task_list, task_detail, user_list, user_detail

admin.site.register(User)


app_name = 'bboard'

router = DefaultRouter()
router.register('rubrics', APIRubricViewSet)

urlpatterns = [
    path('add/', BbCreateView.as_view(), name='add'),
    path('edit/<int:pk>/', BbEditView.as_view(), name='edit'),
    path('delete/<int:pk>/', BbDeleteView.as_view(), name='delete'),

    path('<int:rubric_id>/', BbRubricBbsView.as_view(), name='by_rubric'),

    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),

    path('search/', search, name='search'),

    path('', index, name='index'),

    path('api/rubrics/<int:pk>/', API)
]

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Другие ваши URL-адреса...
]


urlpatterns = [
    path('tasks/', task_list, name='task_list'),  # Получение всех задач и создание новой
    path('tasks/<int:task_id>/', task_detail, name='task_detail'),  # Получение одной задачи и удаление
]



urlpatterns = [
    path('tasks/', task_list, name='task_list'),  # Получение всех задач и создание новой
    path('tasks/<int:task_id>/', task_detail, name='task_detail'),  # Получение одной задачи и удаление
    path('users/', user_list, name='user_list'),  # Получение всех пользователей
    path('users/<int:user_id>/', user_detail, name='user_detail'),  # Получение конкретного пользователя
]







