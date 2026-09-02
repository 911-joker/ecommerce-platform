from django import forms
from django.forms import inlineformset_factory

from store.models import (
    Product,
    ProductVariant,
    Category,
)


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