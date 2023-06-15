from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from cms.menu_bases import CMSAttachMenu
from menus.base import NavigationNode
from menus.menu_pool import menu_pool

from blog.models import Article


class BlogMenu(CMSAttachMenu):
    name = _("Blog Menu")  # give the menu a name this is required.

    def get_nodes(self, request):
        """
        This method is used to build the menu tree.
        """
        nodes = []
        for artic in Article.objects.all():
            node = NavigationNode(
                title=artic.title,
                url=reverse('blog:article_detail', args=(artic.pk,)),
                id=artic.pk,  # unique id for this node within the menu
            )
            nodes.append(node)
        return nodes


menu_pool.register_menu(BlogMenu)
