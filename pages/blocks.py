from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class PictureBlock(blocks.StructBlock):
    """for uploading images"""

    caption = blocks.CharBlock(required=False)

    image = ImageChooserBlock(required=True)
