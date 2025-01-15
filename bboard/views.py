from django.db.models import Count
from django.http import (HttpResponse, HttpResponseRedirect, HttpResponseNotFound,
                         Http404, StreamingHttpResponse, FileResponse, JsonResponse)
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.template import loader
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import (require_http_methods,
                                          require_GET, require_POST, require_safe)
from django.core.paginator import Paginator
from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView

from bboard.forms import BbForm, SearchForm
from bboard.models import Bb, Rubric

from django.shortcuts import render
from datetime import datetime

from django.shortcuts import render

from django.shortcuts import render, redirect
from .forms import IceCreamForm

from django.shortcuts import render, get_object_or_404
from .models import User
from .forms import UserForm


# Основной (вернуть)
def index(request):
    bbs = Bb.objects.order_by('-published')
    # rubrics = Rubric.objects.all()
    rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
    context = {'bbs': bbs, 'rubrics': rubrics}

    return render(request, 'bboard/index.html', context)


def index(request):
    bbs = Bb.objects.order_by('-published')
    rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)

    paginator = Paginator(bbs, 2)

    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1

    page = paginator.get_page(page_num)

    # context = {'bbs': page.objects_list, 'rubrics'}







def by_rubric(request, rubric_id):
    # bbs = Bb.objects.filter(rubric=rubric_id)
    bbs = get_list_or_404(Bb, rubric=rubric_id)
    # rubrics = Rubric.objects.all()
    rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
    current_rubric = Rubric.objects.get(pk=rubric_id)

    # bbs = current_rubric.entries.all()

    context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric}

    return render(request, 'bboard/by_rubric.html', context)


# class BbRubricBbsView(TemplateView):
#     template_name = 'bboard/rubric_bbs.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['bbs'] = Bb.objects.filter(rubric=context['rubric_id'])
#         context['rubrics'] = Rubric.objects.annotate(
#             cnt=Count('bb')).filter(cnt__gt=0)
#         context['current_rubric'] = Rubric.objects.get(pk=context['rubric_id'])
#         return context


class BbRubricBbsView(ListView):
    template_name = 'bboard/rubric_bbs.html'
    context_object_name = 'bbs'

    def get_queryset(self):
        return Bb.objects.filter(rubric=self.kwargs['rubric_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.annotate(
                                            cnt=Count('bb')).filter(cnt__gt=0)
        context['current_rubric'] = Rubric.objects.get(
                                                   pk=self.kwargs['rubric_id'])
        return context


class BbRubricRubbsView(SingleObjectMixin, ListView):
    template_name = 'bboard/rubric_bbs.html'
    pk_url_kwarg = 'rubric_id'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Rubric)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        self.object = self.get_context_data(**kwargs)
        # context['rubrics'] = Rubric.objects.annotate()
# Основной (вернуть)
class BbCreateView(CreateView):
    template_name = 'bboard/bb_create.html'
    model = Bb
    form_class = BbForm
    success_url = reverse_lazy('bboard:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.annotate(
                                            cnt=Count('bb')).filter(cnt__gt=0)
        return context


# class BbCreateView(View):
#     def get(self, request, *args, **kwargs):
#         form = BbForm()
#         context = {'form': form, 'rubrics': Rubric.objects.annotate(
#             cnt=Count('bb')).filter(cnt__gt=0)}
#         return render(request, 'bboard/bb_create.html', context)
#
#     def post(self, request, *args, **kwargs):
#         form = BbForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('bboard:by_rubric',
#                             rubric_id=form.cleaned_data['rubric'].pk)
#         else:
#             context = {'form': form, 'rubrics': Rubric.objects.annotate(
#                 cnt=Count('bb')).filter(cnt__gt=0)}
#             return render(request, 'bboard/bb_create.html', context)


# class BbCreateView(FormView):
#     template_name = 'bboard/bb_create.html'
#     form_class = BbForm
#     initial = {'price': 0.0}
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['rubrics'] = Rubric.objects.annotate(
#                                             cnt=Count('bb')).filter(cnt__gt=0)
#         return context
#
#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)
#
#     def get_form(self, form_class=None):
#         self.object = super().get_form(form_class)
#         return self.object
#
#     def get_success_url(self):
#         return reverse('bboard:by_rubric',
#             kwargs={'rubric_id': self.object.cleaned_data['rubric'].pk})


def add_and_save(request):
    if request.method == 'POST':
        bbf = BbForm(request.POST)
        if bbf.is_valid():
            bbf.save()
            # return HttpResponseRedirect(reverse('bboard:by_rubric',
            #             kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
            return redirect('bboard:by_rubric',
                            rubric_id=bbf.cleaned_data['rubric'].pk)
        else:
            context = {'form': bbf}
            return render(request, 'bboard/bb_create.html', context)
    else:
        bbf = BbForm()

        context = {'form': bbf}
        return render(request, 'bboard/bb_create.html', context)


class BbEditView(UpdateView):
    model = Bb
    form_class = BbForm
    success_url = reverse_lazy('bboard:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.annotate(
                                            cnt=Count('bb')).filter(cnt__gt=0)
        return context


def bb_detail(request, bb_id):
    try:
        # bb = Bb.objects.get(pk=bb_id)
        bb = get_object_or_404(Bb, pk=bb_id)
    except Bb.DoesNotExist:
        # return HttpResponseNotFound('Такое объявление не существует')
        return Http404('Такое объявление не существует')

    rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
    context = {'bb': bb, 'rubrics': rubrics}

    return render(request, 'bboard/bb_detail.html', context)


class BbDetailView(DetailView):
    model = Bb

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.annotate(
                                            cnt=Count('bb')).filter(cnt__gt=0)
        return context


class BbDeleteView(DeleteView):
    model = Bb
    success_url = '/{rubric_id}/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.annotate(
                                            cnt=Count('bb')).filter(cnt__gt=0)
        return context


def example_view(request):
    data = {
        'name': 'Django Example',
        'created_at': datetime.now(),
        'description': None,
    }
    return render(request, 'example_template.html', {'data': data})




def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')


def create_ice_cream(request):
    if request.method == 'POST':
        form = IceCreamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = IceCreamForm()

    return render(request, 'create_ice_cream.html', {'form': form})


def search(request):
    if request.method == 'POST':
        sf = SearchForm(request.POST)
        if sf.is_valid():
            keyword = sf.cleaned_data['keyword']
            rubric_id = sf.cleaned_data['rubric'].pk
            bbs = Bb.objects.filter(title__icontains=keyword,
                                    rubric=rubric_id)
            context = {'bbs': bbs}
            return render(request, 'bboard/search_results/html', context)
    else:
        sf = SearchForm()

    context = {'form': sf}
    return render(request, 'bboard/search.html', context)



def user_list(request):
    users = User.objects.all()
    return render(request, 'users/user_list.html', {'users': users})

def user_detail(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user_id']
            user = get_object_or_404(User, id=user_id)
            return render(request, 'users/user_detail.html', {'user': user})
    else:
        form = UserForm()
    return render(request, 'users/user_detail.html', {'form': form})
