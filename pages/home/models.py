from django.db import models
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.models import Page, Orderable
from wagtail import fields
from modelcluster.fields import ParentalKey
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

    link = models.URLField(
        blank=False,
        null=False,
        help_text="Please provide a YouTube embed link",
        default="http://localhost:5000",
        unique=False,
    )

    text = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        default="Read More",
    )

    panels = [
        FieldPanel("image"),
        FieldPanel("heading"),
        FieldPanel("subheading"),
        FieldPanel("link"),
        FieldPanel("text"),
    ]


class HomePageAboutSection(Orderable):
    page = ParentalKey("home.HomePage", related_name="about_section")  # type: ignore

    section_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    section_heading = models.CharField(
        null=False,
        blank=False,
        max_length=100,
        default="GEO-LDN FLAGSHIP",
    )

    section_subheading = models.CharField(
        max_length=150,
        null=False,
        blank=True,
        default="Enhancing co-operation between Earth observation data providers and Governments.",
    )

    section_content = fields.StreamField(
        [
            (
                "content",
                blocks.RichTextBlock(
                    required=False,
                    help_text="A brief piece of information about the corporation",
                ),
            ),
        ],
        use_json_field=True,
        max_num=1,
        blank=True,
    )

    action_link = models.URLField(
        blank=False,
        null=False,
        help_text="Please provide a YouTube embed link",
        default="http://localhost:5000",
        unique=False,
    )

    action_text = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        default="Read More",
    )

    panels = [
        FieldPanel("section_image"),
        FieldPanel("section_heading"),
        FieldPanel("section_subheading"),
        FieldPanel("section_content"),
        FieldPanel("action_link"),
        FieldPanel("action_text"),
    ]


class HomePageKeyFocusArea(Orderable):
    page = ParentalKey("home.HomePage", related_name="key_focus_area_section")  # type: ignore

    focus_icon = models.CharField(
        null=True,
        blank=False,
        default="ri-bubble-chart-line",
        max_length=70,
    )

    focus_heading = models.CharField(
        null=False,
        blank=False,
        max_length=150,
        help_text="Key focus area content (not more than 250 words)",
        default="GEO-LDN FLAGSHIP",
    )

    focus_content = fields.StreamField(
        [
            (
                "content",
                blocks.RichTextBlock(
                    required=False,
                    help_text="A brief piece of information about the corporation",
                ),
            ),
        ],
        use_json_field=True,
        max_num=1,
        blank=True,
    )

    focus_link = models.URLField(
        blank=False,
        null=True,
        default="http://localhost:5000",
        help_text="Which page to redirect to",
    )

    panels = [
        FieldPanel("focus_heading"),
        FieldPanel("focus_content"),
        FieldPanel("focus_link"),
        FieldPanel("focus_icon"),
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
            max_num=4,
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
            max_num=6,
            min_num=3,
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
