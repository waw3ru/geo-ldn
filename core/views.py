from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
# Standard Python Library imports.
from functools import reduce
import operator

# Core Django imports.
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
    DetailView,
    ListView, UpdateView, CreateView, View
)
from core.models import ToolDetail
# Create your views here.


class ToolDetailView(DetailView):
    model = ToolDetail
    template_name = 'site/tool-details.html'

    def get_context_data(self, **kwargs):
        kwargs['related_tools'] = \
            ToolDetail.objects.all().order_by('year_developed')[:3]
        kwargs['tool'] = self.object
        return super().get_context_data(**kwargs)
