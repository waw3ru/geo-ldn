from django.shortcuts import render
from .models import Event
from datetime import datetime
from django.views.generic import FormView, CreateView, DetailView, ListView, UpdateView, TemplateView

# Create your views here.
# Create your views here.
today = datetime.now().date()


class EventsView(TemplateView):
    template_name = "site/events.html"

    def futureevents(self):
        return Event.objects.filter(event_start_date__gt=today)


class EventDetailViewOld(DetailView):
    queryset = Event.objects.filter(approved=True)
    context_object_name = 'event_details'
    template_name = 'site/event_details.html'

    def this_month_events(self):
        return Event.objects.exclude(pk=self.object.pk).filter(event_start_date__month=today.month, approved=True)


class EventDetailView(DetailView):
    model = Event
    template_name = 'site/event-details.html'

    def get_context_data(self, **kwargs):
        kwargs['related_events'] = \
            Event.objects.all().order_by('-event_end_date')
        kwargs['event'] = self.object
        return super().get_context_data(**kwargs)
