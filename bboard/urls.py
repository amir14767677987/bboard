from django.urls import path, re_path
from django.views.generic.edit import CreateView
from bboard.mode; import Bb
from bboard.views import index, by_rubric, BbCreateView, add, add_save, add_and_save

app_name = 'bboard'

vals = {'mode': 'index'}

urlpatterns = [
    # path('add/save/', add_save, name='add_save'),
    # path('add/', add, name='index'),
    path('add'/, add_and_save, name='add'),
    path('add/', CreateView.as_view(model=Bb,
                        template_name='bboard/bb_create.html'),  name='add'),


    path('add/save/', add_save, name='add_save'),
    path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('', index, name='index')


#     path(r'add/$', BbCreateView.as_view(), name='add'),
#     path(r'^(?P<rubric_id>/[0-9]*)$', by_rubric, name='by_rubric'),
#     path(r'^$', index, name='index'),
]
