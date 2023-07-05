from wagtail import blocks

from pages.blocks import PictureBlock


class AboutSectionBlock(blocks.StructBlock):
    image = PictureBlock()

    heading = blocks.CharBlock(
        max_length=70,
        required=True,
        default="GEO-LDN FLAGSHIP",
    )

    section_content = blocks.RichTextBlock(
        required=True, help_text="A brief piece of information about the corporation"
    )

    subheading = blocks.CharBlock(
        max_length=100,
        required=False,
        default="Enhancing co-operation between Earth observation data providers and Governments.",
    )


class FocusAreaBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=True,
        max_length=100,
        help_text="Key focus area title (not more than 150 words)",
    )

    icon = blocks.CharBlock(
        max_length=70,
        required=True,
    )
    content = blocks.BlockQuoteBlock(
        required=True,
        max_length=255,
        help_text="Key focus area content (not more than 250 words)",
    )

    related_link = blocks.URLBlock(
        required=True,
        help_text="Which page to redirect to",
    )
