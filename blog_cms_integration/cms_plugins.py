from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from blog_cms_integration.models import ArticlePluginModel
from django.utils.translation import gettext as _


@plugin_pool.register_plugin  # register the plugin
class ArticlePluginPublisher(CMSPluginBase):
    model = ArticlePluginModel  # model where plugin data are saved
    module = _("Blog")
    name = _("Article Plugin")  # name of the plugin in the interface
    render_template = "site/blog/blog_plugin.html"

    def render(self, context, instance, placeholder):
        context.update({'instance': instance})
        return context
