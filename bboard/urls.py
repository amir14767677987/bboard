from django.urls import path
from django.views.generic.edit import CreateView
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from bboard.models import Bb
from bboard.views import (index, by_rubric, BbCreateView,
                          add_and_save, bb_detail, BbRubricBbsView,
                          BbDetailView, BbEditView, BbDeleteView,
                          BbRedirectView, edit, rubrics, bbs, search)

from django.contrib import admin
from .models import User

admin.site.register(User)


app_name = 'bboard'

urlpatterns = [
    path('add/', BbCreateView.as_view(), name='add'),
    path('edit/<int:pk>/', BbEditView.as_view(), name='edit'),
    path('delete/<int:pk>/', BbDeleteView.as_view(), name='delete'),

    path('<int:rubric_id>/', BbRubricBbsView.as_view(), name='by_rubric'),

    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),

    path('search/', search, name='search'),

    path('', index, name='index'),
]



urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Другие ваши URL-адреса...
]




