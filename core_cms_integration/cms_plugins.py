from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from core_cms_integration.models import ToolPluginModel
from django.utils.translation import gettext as _


@plugin_pool.register_plugin  # register the plugin
class ToolPlugin(CMSPluginBase):
    model = ToolPluginModel  # model where plugin data are saved
    module = _("Tools")
    name = _("Tool Plugin")  # name of the plugin in the interface
    render_template = "site/tool_plugin.html"

    def render(self, context, instance, placeholder):
        context.update({'instance': instance})
        return context
