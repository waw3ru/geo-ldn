from django.db import models
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.models import Page, Orderable
from wagtail import fields
from modelcluster.fields import ParentalKey
from pages.home.blocks import AboutSectionBlock
from pages.model_utils import PAGE_LEVELS


class HomePageCarousel(Orderable):
    page = ParentalKey("home.HomePage", related_name="carousel_images")  # type: ignore

    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    heading = models.CharField(
        max_length=125,
        blank=False,
        null=False,
        default="Land Degradation Neutrality Initiative",
    )

    subheading = models.CharField(
        max_length=150,
        null=False,
        blank=False,
        default="GEO-LDN is a stakeholder-driven initiative that aims to boost co-operation between Earth observation data providers and Governments.",
    )

    panels = [
        FieldPanel("image"),
        FieldPanel("heading"),
        FieldPanel("subheading"),
    ]


class HomePageAboutSection(Orderable):
    page = ParentalKey("home.HomePage", related_name="about_section")  # type: ignore

    body = fields.StreamField(
        AboutSectionBlock(),
        use_json_field=True,
        min_num=1,
        max_num=4,
        block_counts={
            "image": {"max_num": 2},
            "heading": {"max_num": 1},
            "section_content": {"max_num": 1},
            "subheading": {"max_num": 1},
        },
    )

    panels = [
        FieldPanel("body"),
    ]


class HomePage(Page):
    class Meta:
        verbose_name = "GEO-LDN Home page"

        verbose_name_plural = "GEO-LDN Home pages"

        permissions = [
            ("can_change_page_level", "Can change the page level"),
        ]

    page_level = models.CharField(default="L1", choices=PAGE_LEVELS, blank=False)

    video_link = models.URLField(
        blank=True,
        null=True,
        help_text="Please provide a YouTube embed link",
        unique=True,
    )

    video_caption = models.TextField(
        max_length=125,
        blank=True,
        null=True,
        default="Land Degradation Neutrality Initiative",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                InlinePanel(
                    "carousel_images",
                    max_num=3,
                    min_num=1,
                    label="Header Slideshow Image",
                    classname="collapsed",
                ),
                InlinePanel(
                    "about_section",
                    max_num=1,
                    min_num=1,
                    label="Page Content",
                    classname="collapsed",
                ),
            ],
            heading="Homepage Content",
        ),
        FieldPanel("video_link"),
        FieldPanel("video_caption"),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel(
            "page_level",
            disable_comments=True,
            permission="page.home.can_change_page_level",
        ),
    ]

    parent_page_types = ["wagtailcore.Page"]

    subpage_types = []

    template = "home.html"

    max_count = 1

    show_in_menus = True
