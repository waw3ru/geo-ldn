from wagtail import blocks

from pages.blocks import PictureBlock


class AboutSectionBlock(blocks.StreamBlock):
    image = PictureBlock()

    heading = blocks.CharBlock(
        form_classname="title",
        max_length=70,
        required=True,
        default="GEO-LDN FLAGSHIP",
    )

    section_content = blocks.RichTextBlock(
        required=True, help_text="A brief piece of information about the corporation"
    )

    subheading = blocks.CharBlock(
        form_classname="subtitle",
        max_length=100,
        required=False,
        default="Enhancing co-operation between Earth observation data providers and Governments.",
    )
