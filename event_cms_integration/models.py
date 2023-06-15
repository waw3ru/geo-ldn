from django.db import models
from cms.models import CMSPlugin
from events.models import Event


class EventPluginModel(CMSPlugin):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.event.name
