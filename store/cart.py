from decimal import Decimal

from .models import Product, ProductVariant


class Cart:
    SESSION_KEY = "cart"

    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.get(
            self.SESSION_KEY,
            {},
        )

    def add(
        self,
        product,
        quantity=1,
        variant=None,
    ):
        # -----------------------------------------------------
        # VARIANT PRODUCT
        # -----------------------------------------------------

        if variant:
            cart_key = f"{product.id}:{variant.id}"

            if cart_key not in self.cart:
                self.cart[cart_key] = {
                    "product_id": product.id,
                    "variant_id": variant.id,
                    "quantity": 0,
                    "price": str(product.price),
                }

            self.cart[cart_key]["quantity"] += quantity

        # -----------------------------------------------------
        # NORMAL PRODUCT
        # -----------------------------------------------------

        else:
            product_id = str(product.id)

            if product_id not in self.cart:
                self.cart[product_id] = {
                    "product_id": product.id,
                    "quantity": 0,
                    "price": str(product.price),
                }

            self.cart[product_id]["quantity"] += quantity

        self.save()

    def remove(
        self,
        product,
        variant=None,
    ):
        if variant:
            cart_key = f"{product.id}:{variant.id}"
        else:
            cart_key = str(product.id)

        if cart_key in self.cart:
            del self.cart[cart_key]
            self.save()

    def update(
        self,
        product,
        quantity,
        variant=None,
    ):
        if quantity <= 0:
            self.remove(
                product,
                variant=variant,
            )
            return

        if variant:
            cart_key = f"{product.id}:{variant.id}"
        else:
            cart_key = str(product.id)

        if cart_key in self.cart:
            self.cart[cart_key]["quantity"] = quantity
            self.save()

    def save(self):
        self.session[self.SESSION_KEY] = self.cart
        self.session.modified = True

    def clear(self):
        self.session.pop(
            self.SESSION_KEY,
            None,
        )

        self.session.modified = True

    def __len__(self):
        return sum(
            item["quantity"]
            for item in self.cart.values()
        )

    def __iter__(self):
        product_ids = {
            str(item["product_id"])
            for item in self.cart.values()
        }

        products = Product.objects.filter(
            id__in=product_ids
        )

        product_map = {
            str(product.id): product
            for product in products
        }

        variant_ids = {
            item["variant_id"]
            for item in self.cart.values()
            if item.get("variant_id")
        }

        variants = ProductVariant.objects.filter(
            id__in=variant_ids
        )

        variant_map = {
            variant.id: variant
            for variant in variants
        }

        for cart_key, item in self.cart.items():

            product = product_map.get(
                str(item["product_id"])
            )

            if not product:
                continue

            price = Decimal(
                item["price"]
            )

            quantity = item["quantity"]

            variant = None

            if item.get("variant_id"):
                variant = variant_map.get(
                    item["variant_id"]
                )

                if not variant:
                    continue

            yield {
                "product": product,
                "variant": variant,
                "variant_id": (
                    variant.id
                    if variant
                    else None
                ),
                "quantity": quantity,
                "price": price,
                "total_price": price * quantity,
            }

    def get_total_price(self):
        return sum(
            item["total_price"]
            for item in self
        )