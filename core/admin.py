from django.contrib import admin
from django.contrib.gis.db import models
from .models import Tool, ToolDetail, ToolDetail
from mapwidgets.widgets import GooglePointFieldWidget
from tinymce.widgets import TinyMCE
# Register your models here.


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'year_developed', 'created_by', 'added_on')
    prepopulated_fields = {'slug': ('name',), }
    exclude = ['created_by', ]
    # summernote_fields = ('description',)
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }


@admin.register(ToolDetail)
class ToolDetailAdmin(admin.ModelAdmin):
    list_display = ('name', 'year_developed', 'created_by', 'added_on')
    prepopulated_fields = {'slug': ('name',), }
    exlude = ['created_by', ]
    # summernote_fields = ('description',)
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }
