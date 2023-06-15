from django.contrib.gis.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.utils.text import slugify
import itertools
from tinymce.widgets import TinyMCE
from djmoney.models.fields import MoneyField
from djmoney.models.validators import MaxMoneyValidator, MinMoneyValidator
from geo import settings
from datetime import datetime
from cms.models import CMSPlugin
from django.core.exceptions import ValidationError


def validator(image, width=None, height=None):
    error = False
    if width is not None and image.width < width:
        error = True
    if height is not None and image.height < height:
        error = True
    if error:
        raise ValidationError(
            [f'Size should be at least {width} x {height} pixels.']
        )
# Create your models here.


def upload_tool_image(instance, filename):
    return '/'.join(['tools', str(instance.id), filename])


class Tool(CMSPlugin):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    feature_image = models.ImageField(upload_to=upload_tool_image,)
    year_developed = models.DateField()
    description = models.TextField(
        null=True, help_text='e.g. An overview of the tool')
    link = models.URLField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Analytical Tools"


class ToolDetail(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    feature_image = models.ImageField(upload_to=upload_tool_image,)
    year_developed = models.DateField()
    description = models.TextField(
        null=True, help_text='e.g. An overview of the tool')
    link = models.URLField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Analytical Tools"
