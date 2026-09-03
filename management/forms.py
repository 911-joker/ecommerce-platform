from django import forms
from django.forms import inlineformset_factory

from wagtail.images import get_image_model

from store.models import (
    Product,
    ProductVariant,
    Category,
)

from home.models import HomePage, HomePageNewArrival


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product

        fields = [
            "title",
            "price",
            "description",
            "category",
        ]

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "placeholder": "Product name",
                }
            ),

            "price": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "min": "0",
                    "placeholder": "0.00",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Product description",
                }
            ),

        }


ProductVariantFormSet = inlineformset_factory(
    Product,
    ProductVariant,

    fields=[
        "sku",
        "color",
        "image",
        "size",
        "stock",
    ],

    extra=0,
    can_delete=True,
)


ProductVariantCreateFormSet = inlineformset_factory(
    Product,
    ProductVariant,

    fields=[
        "sku",
        "color",
        "image",
        "size",
        "stock",
    ],

    extra=1,
    can_delete=True,
)


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category

        fields = [
            "name",
            "slug",
        ]

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "placeholder": "Category name",
                }
            ),

            "slug": forms.TextInput(
                attrs={
                    "placeholder": "category-slug",
                }
            ),

        }


class HomePageForm(forms.ModelForm):
    class Meta:
        model = HomePage
        fields = [
            "hero_image",
            "hero_eyebrow",
            "hero_title",
            "hero_description",

            "men_image",
            "women_image",

            "category_eyebrow",
            "category_title",
            "category_description",
            "men_title",
            "women_title",

            "new_arrivals_eyebrow",
            "new_arrivals_title",

            "editorial_image",
            "editorial_eyebrow",
            "editorial_title",
            "editorial_description",
        ]

        widgets = {
            "hero_eyebrow": forms.TextInput(
                attrs={
                    "placeholder": "NEW COLLECTION",
                }
            ),
            "hero_title": forms.TextInput(
                attrs={
                    "placeholder": "Style Made For You.",
                }
            ),
            "hero_description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Discover our latest collection of modern fashion.",
                }
            ),
        }


class NewArrivalForm(forms.ModelForm):
    class Meta:
        model = HomePageNewArrival
        fields = ["product"]


class MediaUploadForm(forms.ModelForm):
    class Meta:
        model = get_image_model()
        fields = [
            "title",
            "file",
        ]