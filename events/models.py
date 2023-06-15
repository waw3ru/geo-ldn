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


class EventPlugin(CMSPlugin):
    event = models.ForeignKey(
        'Event', related_name='plugins', on_delete=models.CASCADE)

    def __str__(self):
        return self.event.name

# Create your models here.


def upload_event_flyer(instance, filename):
    return '/'.join(['events', str(instance.id), filename])


event_status = (
    ('Upcoming', 'Upcoming'),
    ('On-Going', 'On-Going'),
    ('Past', 'Past'),
)


class Event(CMSPlugin):
    name = models.CharField(
        max_length=100, help_text="e.g. Google Earth Training")
    slug = models.SlugField()
    theme = models.CharField(max_length=50, null=True,
                             help_text='i.e Food Security in Africa')
    event_start_date = models.DateField()
    event_end_date = models.DateField()
    event_start_time = models.TimeField(null=True)
    event_end_time = models.TimeField(null=True)
    organiser = models.CharField(
        max_length=50, null=True, help_text='i.e Food Security in Africa')
    description = models.TextField(
        null=True, help_text='e.g. An overview of the event')
    flyer = models.ImageField(
        upload_to=upload_event_flyer, help_text="Upload photo or flyer for the event")
    contact_email = models.EmailField(null=True, blank=True)
    contact_mobile = PhoneNumberField(null=True, blank=True)
    charges = MoneyField(max_digits=14, decimal_places=2, default_currency='USD',
                         null=True, blank=True, validators=[
                             MinMoneyValidator(0), ])
    date_added = models.DateField(auto_now_add=True)
    virtual_event_link = models.URLField(blank=True, null=True)
    status = models.CharField(
        max_length=15, null=False, choices=event_status, default=event_status[0][0])
    approved = models.BooleanField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    geom = models.PointField(srid=4326, null=True, blank=True)

    def __str__(self):
        return self.slug

    def calculate_time_left(self):
        today = datetime.now().date()
        return (self.event_start_date - today).days

    class Meta:
        verbose_name_plural = "Events"

    @property
    def image_size(self):
        return settings.EVENTS_DEFAULT_EVENT_SIZE

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = original = slugify(self.name)
            for x in itertools.count(1):
                if not Event.objects.filter(slug=self.slug).exists():
                    break
                self.slug = '%s-%d' % (original, x)
        super(Event, self).save(*args, **kwargs)
