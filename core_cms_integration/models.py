from django.db import models
from cms.models import CMSPlugin
from core.models import ToolDetail


class ToolPluginModel(CMSPlugin):
    tool = models.ForeignKey(ToolDetail, on_delete=models.CASCADE)

    def __str__(self):
        return self.tool.name
