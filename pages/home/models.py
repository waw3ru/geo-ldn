from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.search import index


class HomePage(Page):
    body = RichTextField(null=True)

    feed_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    search_fields = Page.search_fields + [
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("body", classname="full"),
    ]

    parent_page_types = ["wagtailcore.Page"]

    template = "home.html"

    def get_context(self, request, *args, **kwargs):
        """Adding HomePage to your page context."""
        context = super().get_context(request, *args, **kwargs)
        pages = []

        for page in Page.objects.live():
            pages.append({"title": page.title, "url": page.slug})

        context["menu_pages"] = pages

        return context
