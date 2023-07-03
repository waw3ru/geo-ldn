from django.db import models
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.models import Page, Orderable
from wagtail.search import index
from wagtail import blocks
from wagtail.fields import StreamField
from modelcluster.fields import ParentalKey


class HomePageCarousel(Orderable):
    page = ParentalKey("home.HomePage", related_name="carousel_images")  # type: ignore

    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    heading = models.CharField(max_length=125)

    paragraph = models.TextField(max_length=255)

    panels = [FieldPanel("image"), FieldPanel("heading"), FieldPanel("paragraph")]


class HomePage(Page):
    page_type = "home-page"

    about_section = StreamField(
        [
            (
                "content",
                blocks.StructBlock(
                    [
                        (
                            "heading",
                            blocks.CharBlock(
                                form_classname="title",
                                max_length=125,
                                null=True,
                            ),
                        ),
                        (
                            "sub_heading",
                            blocks.CharBlock(
                                form_classname="subtitle",
                                max_length=255,
                                null=True,
                            ),
                        ),
                        ("content", blocks.RichTextBlock(blank=True)),
                    ],
                ),
            ),
            (
                "images",
                blocks.StructBlock(
                    [
                        ("caption", blocks.CharBlock()),
                        ("url", blocks.URLBlock()),
                    ],
                ),
            ),
            ("video", blocks.URLBlock()),
        ],
        use_json_field=True,
        default=None,
        block_counts={
            "content": {"max_num": 1},
            "images": {"max_num": 1},
            "video": {"max_num": 1},
        },
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [InlinePanel("carousel_images", max_num=5, min_num=1, label="Image")],
            heading="Carousel Images",
        ),
        FieldPanel("about_section"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("about_section"),
    ]

    parent_page_types = ["wagtailcore.Page"]

    subpage_types = []

    template = "home.html"

    max_count = 1

    def get_context(self, request, *args, **kwargs):
        """Adding HomePage to your page context."""
        context = super().get_context(request, *args, **kwargs)
        pages = []

        for page in Page.objects.live().is_menu().public():
            pages.append({"title": page.title, "url": page.slug})

        context["menu_pages"] = pages

        return context
