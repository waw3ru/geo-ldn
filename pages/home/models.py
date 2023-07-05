from django.db import models
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.models import Page, Orderable
from wagtail import fields
from modelcluster.fields import ParentalKey
from pages.blocks import ButtonBlock
from pages.home.blocks import AboutSectionBlock, FocusAreaBlock
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

    action_button = fields.StreamField(
        [
            ("call_to_action", ButtonBlock()),
        ],
        use_json_field=True,
        max_num=1,
        blank=True,
    )

    panels = [
        FieldPanel("image"),
        FieldPanel("heading"),
        FieldPanel("subheading"),
        FieldPanel("action_button"),
    ]


class HomePageAboutSection(Orderable):
    page = ParentalKey("home.HomePage", related_name="about_section")  # type: ignore

    about_section_content = fields.StreamField(
        [
            (
                "content",
                AboutSectionBlock(),
            ),
        ],
        use_json_field=True,
        max_num=1,
        blank=True,
    )

    action_button = fields.StreamField(
        [
            ("call_to_action", ButtonBlock()),
        ],
        use_json_field=True,
        max_num=1,
        blank=True,
    )

    panels = [
        FieldPanel("about_section_content"),
        FieldPanel("action_button"),
    ]


class HomePageKeyFocusArea(Orderable):
    page = ParentalKey("home.HomePage", related_name="key_focus_area_section")  # type: ignore

    key_focus_areas = fields.StreamField(
        [
            (
                "content",
                FocusAreaBlock(),
            ),
        ],
        use_json_field=True,
        max_num=6,
        blank=True,
    )

    panels = [
        FieldPanel("key_focus_areas"),
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
        InlinePanel(
            "carousel_images",
            max_num=3,
            min_num=1,
            label="Slideshow",
            classname="collapsed",
        ),
        InlinePanel(
            "about_section",
            max_num=1,
            min_num=1,
            label="About Section",
            classname="collapsed",
        ),
        InlinePanel(
            "key_focus_area_section",
            max_num=1,
            min_num=1,
            label="Key Focus Area",
            classname="collapsed",
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
