from django.db import models

from wagtail.admin.panels import FieldPanel
from wagtail.images import get_image_model_string
from wagtail.models import Page


class HomePage(Page):

    hero_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    hero_eyebrow = models.CharField(
        max_length=100,
        default="NEW COLLECTION",
    )

    hero_title = models.CharField(
        max_length=200,
        default="Style Made For You.",
    )

    hero_description = models.TextField(
        blank=True,
        default="Discover our latest collection of modern fashion.",
    )

    men_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    women_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    editorial_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [

        FieldPanel("hero_image"),
        FieldPanel("hero_eyebrow"),
        FieldPanel("hero_title"),
        FieldPanel("hero_description"),

        FieldPanel("men_image"),
        FieldPanel("women_image"),

        FieldPanel("editorial_image"),
    ]