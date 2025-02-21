from django.contrib import admin

from bboard.models import Rubric, Bb


class BbAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'price', 'published', 'rubric' )
    # list_display = ('title_and_price', 'content', 'published', 'rubric')
    # list_display = ('title_and_price', 'content', 'price', 'published',)

    @admin.display(description='Назвние и рубрика', ordering='title')
    def title_and_rubric(self, rec):
        return f'{rec.title} ({rec.rubric.name})'

    list_editable = ('title', 'content', 'price', 'rubric')


class RubricAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'price', 'published', 'rubric')


class PriceListFilter(admin.SimpleListFilter):
    title = 'Категория'


admin.site.register(Rubric)
admin.site.register(Bb, BbAdmin)



