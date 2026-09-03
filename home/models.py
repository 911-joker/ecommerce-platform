from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.images import get_image_model_string
from wagtail.models import Page, Orderable


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

    category_eyebrow = models.CharField(
        max_length=100,
        default="EXPLORE",
    )

    category_title = models.CharField(
        max_length=200,
        default="Find Your Style.",
    )

    category_description = models.TextField(
        blank=True,
        default="Explore our collections designed for every style, occasion and everyday moment.",
    )

    men_title = models.CharField(
        max_length=100,
        default="Men",
    )

    women_title = models.CharField(
        max_length=100,
        default="Women",
    )

    new_arrivals_eyebrow = models.CharField(
        max_length=100,
        default="DISCOVER",
    )

    new_arrivals_title = models.CharField(
        max_length=200,
        default="New Arrivals",
    )

    editorial_eyebrow = models.CharField(
        max_length=100,
        default="THE COLLECTION",
    )

    editorial_title = models.CharField(
        max_length=200,
        default="Elevate Your Everyday.",
    )

    editorial_description = models.TextField(
        blank=True,
        default="Discover pieces designed to make every moment feel effortless.",
    )
    

    content_panels = Page.content_panels + [

        FieldPanel("hero_image"),
        FieldPanel("hero_eyebrow"),
        FieldPanel("hero_title"),
        FieldPanel("hero_description"),

        FieldPanel("men_image"),
        FieldPanel("women_image"),

        FieldPanel("editorial_image"),

        FieldPanel("category_eyebrow"),
        FieldPanel("category_title"),
        FieldPanel("category_description"),
        FieldPanel("men_title"),
        FieldPanel("women_title"),
        FieldPanel("new_arrivals_eyebrow"),
        FieldPanel("new_arrivals_title"),

        InlinePanel(
            "new_arrivals",
            label="New Arrival Products",
            heading="Products shown in New Arrivals",
        ),
        
        FieldPanel("editorial_eyebrow"),
        FieldPanel("editorial_title"),
        FieldPanel("editorial_description"),
    ]


class HomePageNewArrival(Orderable):
    page = ParentalKey(
        "home.HomePage",
        on_delete=models.CASCADE,
        related_name="new_arrivals",
    )

    product = models.ForeignKey(
        "store.Product",
        on_delete=models.CASCADE,
        related_name="homepage_new_arrivals",
    )

    panels = [
        FieldPanel("product"),
    ]