from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.models import Page, Orderable
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey

@register_snippet
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class ShopPage(Page):
    parent_page_types = ["home.HomePage"]
    subpage_types = ["store.Product"]

    content_panels = Page.content_panels

class Product(Page):
    parent_page_types = ["store.ShopPage"]

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    description = models.TextField(
        blank=True,
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
    )

    content_panels = Page.content_panels + [
        FieldPanel("price"),
        FieldPanel("description"),
        FieldPanel("category"),

        InlinePanel(
            "variants",
            label="Clothing Variants",
            heading="Size & Color Variants",
        ),
    ]

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

class ProductVariant(Orderable):
    SIZE_CHOICES = [
        ("XS", "XS"),
        ("S", "S"),
        ("M", "M"),
        ("L", "L"),
        ("XL", "XL"),
        ("XXL", "XXL"),
        ("ONE_SIZE", "One Size"),
    ]

    product = ParentalKey(
        "store.Product",
        on_delete=models.CASCADE,
        related_name="variants",
    )

    sku = models.CharField(
        max_length=100,
        unique=True,
    )

    color = models.CharField(
        max_length=50,
    )

    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )

    size = models.CharField(
        max_length=20,
        choices=SIZE_CHOICES,
    )

    stock = models.PositiveIntegerField(
        default=0,
    )

    panels = [
        FieldPanel("sku"),
        FieldPanel("color"),
        FieldPanel("image"),
        FieldPanel("size"),
        FieldPanel("stock"),
    ]

    def __str__(self):
        return f"{self.product.title} — {self.color} / {self.size}"

class CustomerProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="customer_profile",
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    address = models.CharField(
        max_length=255,
        blank=True,
    )

    city = models.CharField(
        max_length=100,
        blank=True,
    )

    state = models.CharField(
        max_length=100,
        blank=True,
    )

    def __str__(self):
        return self.user.username


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("processing", "Processing"),
        ("shipped", "Shipped"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    total = models.DecimalField(max_digits=12, decimal_places=2)

    paystack_reference = models.CharField(max_length=100, unique=True, null=True, blank=True,)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE,
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="order_items",
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    quantity = models.PositiveIntegerField()


    @property
    def subtotal(self):

        return self.price * self.quantity


    def __str__(self):

        if self.variant:

            return (
                f"{self.product.title} "
                f"({self.variant.color} / {self.variant.size}) "
                f"x {self.quantity}"
            )

        return (
            f"{self.product.title} "
            f"x {self.quantity}"
        )