# from django.contrib import admin
#
# from .models import Article
#
#
# @admin.register(Article)
# class ArticleAdmin(admin.ModelAdmin):
#     pass

from django.contrib import admin
from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError
from .models import Article, Tag, Scope


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        main_tags_count = sum(1 for form in self.forms if form.cleaned_data.get('is_main'))

        if main_tags_count == 0:
            raise ValidationError('У статьи должен быть один основной раздел.')
        elif main_tags_count > 1:
            raise ValidationError('У статьи может быть только один основной раздел.')

        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
