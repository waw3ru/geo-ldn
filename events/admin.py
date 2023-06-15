from django.contrib import admin
from django.contrib.gis.db import models
from .models import Event
from mapwidgets.widgets import GooglePointFieldWidget
from tinymce.widgets import TinyMCE
# Register your models here.


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_start_date', 'event_end_date', 'organiser')
    # summernote_fields = ('description',)
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget},
        models.TextField: {'widget': TinyMCE()}
    }
