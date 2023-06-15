from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from events.models import Event
from django.utils.translation import ugettext as _
from datetime import datetime
from event_cms_integration.models import EventPluginModel

today = datetime.now().date()


@plugin_pool.register_plugin
class EventPlugin(CMSPluginBase):
    model = EventPluginModel  # Model where data about this plugin is saved
    module = _("Events")
    name = _("Event Plugin")  # Name of the plugin
    render_template = "site/event_listing.html"

    def render(self, context, instance, placeholder):
        context.update({'instance': instance})
        return context

    # def render(self, context, instance, placeholder):
    #     event_list = Event.objects.filter(
    #         approved=True)
    #     context.update({'events': event_list})
    #     return context


# class DocumentationPlugin(CMSPluginBase):
#     model = CMSPlugin
#     name = _("Documentation Plugin")
#     render_template = "site/documentation_listing.html"
#     cache = False


@plugin_pool.register_plugin
class UserAccountPlugin(CMSPluginBase):
    model = CMSPlugin
    render_template = "site/logged_user.html"
    cache = False
