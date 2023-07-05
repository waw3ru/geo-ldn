from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class PictureBlock(blocks.StructBlock):
    """for uploading images"""

    caption = blocks.CharBlock(required=False)

    image = ImageChooserBlock(required=True)


class ButtonBlock(blocks.StructBlock):
    """for call to action buttons"""

    link = blocks.URLBlock(required=True)

    text = blocks.CharBlock(max_length=50, required=True)
