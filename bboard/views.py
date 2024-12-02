from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView

from bboard.forms import BbForm
from bboard.models import Bb, Rubric


def index(request):
     # Todo:Удалить
     print(request.scheme)
     print(request.path)
     print(request.path_info)
     print(request.encoding)
     print(request.content_type)
     print(request.content_params)
     print(request.headers['Accept-Encoding'])
     print(request.META)
     print(request.META['CONTENT_TYPE'])
     print(request.META['HTTP_HOST'])
     print(request.META['HTTP_USER_AGENT'])
     print(request.META['HTTP_REFERER'])
     # Todo:Удалить


     bbs = Bb.objects.order_by('-published')
     rubrics = Rubric.objects.annotate(cnt=Count)
     context = {'bbs': bbs, 'rubrics': rubrics}

     return render(request, 'bboard/index.html', context)


# def index(request):
#     resp = HttpResponse('Здесь будет', content_type='text/plain')
#     resp.write('главная')
#     resp.writelines(('страница', 'сайта'))
#     resp['keywords'] = 'Python, Django'
#     return resp


# def index(request):
#     bbs = Bb.objects.all()
#     rubrics = Rubric.objects.all()
#     context = {'bbs': bbs, 'rubrics': rubrics}
#     from django.template.loader import get_template
#     template = get_template('bboard/index.html')
#     return HttpResponse(template.render(context, request))


# def by_rubric(request, rubric_id, mode):
def by_rubric(request, rubric_id, mode):
    bbs = Bb.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.all()
    current_rubric = Rubric.objects.get(pk=rubric_id)

    # bbs = current_rubric.entries.all()

    context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric}

    return render(request, 'bboard/by_rubric.html', context)


class BbCreateView(CreateView):
    template_name = 'bboard/create.html'
    # form_class = BbForm
    success_url = reverse_lazy('bboard:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all(cnt=Count('bb')).filter()
        return context

def add(request):
    bbf = BbForm()
    context = {'form': bbf}
    return render(request, 'bboard/bb_create', context)


def add_save(request):
    bbf = BbForm(request.POST)
    if bbf.is_valid():
        bbf.save()
        return HttpResponseRedirect(reverse('bboard:by_rubric', kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
    else:
        context = {'form': bbf}
        return render(request, 'bboard/bb_create', context)

class BbCreateView(View):
    def get(self, request, *args, **kwargs):
        form = BbForm()
        context = {'form': form, 'rubrics': Rubric.objects.annotate(
            cnt=Count('bb')).filter(cnt__gt=0)}
        return render(request, 'bboard/bb_create.html', context)
     def post(selfseld, request, *args, **kwargs):
         form = BbForm(request.POST)
         if form.is_valid():
             form.save()
             return redirect('bboard:by_rubric',
                             rubric_id=form.cleaned_data['rubric'].pk)
        else:
    context = {}

class BbRubricBbsView(TemplateView):
    templates_name = 'bboard/rubric_bbs.html'
    def get_context_data



def add_and_save(request):
    if request.method == 'POST':
        bbf = BbForm(request.POST)
        if bbf.is_valid():
            bbf.save()
            return HttpResponseRedirect(reverse('bboard:by_rubric', kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
        else:
            context = {'form': bbf}
            return render(request, 'bboard/bb_create', context)
    else:
        bbf = BbForm()
        context = {'form': bbf}
        return render(request, 'bboard/bb_create.html', context)

    # def bb_detali(request, bb_id):
    #     try:
    #         bb = Bb.objects.get(pk=bb_id)
    #     except BbDoesNotExist:
    #     return HttpResponseNotFound('Такое объявление не существует')
    return Http404('Такое объявление не существует ')
    #
    # rubrics = Rubric.objects.all(cnt=Count('bb')).filter()
    # context = {'bb': bb, 'rubrics': rubrics}
    #
    # return render(request, 'bboard/bb_detali', context)
    #
