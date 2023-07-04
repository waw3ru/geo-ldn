from django.db import models
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.models import Page, Orderable
from wagtail.search import index
from wagtail import blocks
from wagtail.images import blocks as image_blocks
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.fields import StreamField


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "blog.BlogPage", on_delete=models.CASCADE, related_name="tagged_items"
    )


class BlogPage(Page):
    page_type = "blog-page"

    image = image_blocks.ImageChooserBlock(required=False)

    title = blocks.CharBlock(
        form_classname="blog-title",
        max_length=125,
        null=True,
    )

    description = blocks.BlockQuoteBlock(
        form_classname="blog-description",
        max_length=255,
        null=True,
    )

    blog_content = StreamField(
        [
            ("heading", blocks.CharBlock(form_classname="blog-title")),
            (
                "description",
                blocks.BlockQuoteBlock(
                    form_classname="blog-description",
                    max_length=255,
                ),
            ),
            ("image", image_blocks.ImageChooserBlock(required=False)),
            ("content", blocks.RichTextBlock(required=True)),
        ],
        block_counts={
            "heading": {"max_num": 1},
            "description": {"max_num": 1},
            "image": {"max_num": 1},
        },
        use_json_field=True,
    )

    last_modified = models.DateTimeField(editable=False, auto_now=True)

    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("blog_content"),
        InlinePanel("related_links", heading="Related links", label="Related link"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("title"),
        index.SearchField("description"),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel("tags"),
    ]

    parent_page_types = ["wagtailcore.Page", "blog.BlogPage"]

    subpage_types = ["blog.BlogPage"]

    template = "blog.html"

    def get_context(self, request, *args, **kwargs):
        """Adding HomePage to your page context."""
        context = super().get_context(request, *args, **kwargs)
        pages = []

        for page in Page.objects.live().public():
            pages.append({"title": page.title, "url": page.slug})

        context["menu_pages"] = pages

        return context


class BlogPageRelatedLink(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name="related_links")

    name = models.CharField(max_length=255)

    url = models.URLField()

    panels = [
        FieldPanel("name"),
        FieldPanel("url"),
    ]
