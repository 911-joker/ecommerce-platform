from django.contrib.auth.decorators import user_passes_test
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from store.models import (
    Product,
    ProductVariant,
    ShopPage,
    Order,
    CustomerProfile,
    Category,
)

from .forms import (
    ProductForm,
    ProductVariantFormSet,
    ProductVariantCreateFormSet,
    CategoryForm,
)


def is_store_owner(user):
    return (
        user.is_authenticated
        and user.is_superuser
    )


def store_owner_required(view_func):
    return user_passes_test(
        is_store_owner,
        login_url="/account/login/",
    )(view_func)


@store_owner_required
def dashboard(request):

    products = Product.objects.all()

    total_products = products.count()

    total_inventory = sum(
        ProductVariant.objects.values_list(
            "stock",
            flat=True
        )
    )

    total_orders = Order.objects.count()

    total_customers = CustomerProfile.objects.count()

    pending_orders = Order.objects.filter(
        status="pending"
    ).count()

    low_stock_variants = ProductVariant.objects.filter(
        stock__lte=5
    ).select_related(
        "product"
    ).order_by(
        "stock"
    )[:5]

    return render(
        request,
        "management/dashboard.html",
        {
            "total_products": total_products,
            "total_inventory": total_inventory,
            "total_orders": total_orders,
            "total_customers": total_customers,
            "pending_orders": pending_orders,
            "low_stock_variants": low_stock_variants,
        },
    )


# =========================================================
# PRODUCTS
# =========================================================

@store_owner_required
def product_list(request):

    products = Product.objects.prefetch_related(
        "variants"
    ).order_by("-id")

    for product in products:
        product.total_stock = sum(
            variant.stock
            for variant in product.variants.all()
        )

    return render(
        request,
        "management/product.html",
        {
            "products": products,
        },
    )


@store_owner_required
def product_create(request):

    shop_page = get_object_or_404(
        ShopPage,
        slug="shop",
    )

    if request.method == "POST":

        form = ProductForm(request.POST)

        if form.is_valid():

            with transaction.atomic():

                product = form.save(commit=False)

                shop_page.add_child(
                    instance=product
                )

                formset = ProductVariantCreateFormSet(
                    request.POST,
                    request.FILES,
                    instance=product,
                )

                if formset.is_valid():

                    formset.save()

                    return redirect(
                        "management:products"
                    )

                product.delete()

    else:

        form = ProductForm()
        formset = ProductVariantCreateFormSet()

    return render(
        request,
        "management/product_form.html",
        {
            "form": form,
            "formset": formset,
        },
    )


@store_owner_required
def product_edit(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
    )

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            instance=product,
        )

        formset = ProductVariantFormSet(
            request.POST,
            request.FILES,
            instance=product,
        )

        if form.is_valid() and formset.is_valid():

            with transaction.atomic():

                form.save()
                formset.save()

            return redirect(
                "management:products"
            )

    else:

        form = ProductForm(
            instance=product,
        )

        formset = ProductVariantFormSet(
            instance=product,
        )

    return render(
        request,
        "management/product_form.html",
        {
            "form": form,
            "formset": formset,
            "editing": True,
            "product": product,
        },
    )


# =========================================================
# ORDERS
# =========================================================

@store_owner_required
def order_list(request):

    orders = Order.objects.prefetch_related(
        "items"
    ).order_by("-created_at")

    return render(
        request,
        "management/orders.html",
        {
            "orders": orders,
        },
    )


@store_owner_required
def order_edit(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
    )

    if request.method == "POST":

        new_status = request.POST.get(
            "status"
        )

        valid_statuses = {
            choice[0]
            for choice in Order.STATUS_CHOICES
        }

        if new_status in valid_statuses:

            order.status = new_status

            order.save(
                update_fields=["status"]
            )

        return redirect(
            "management:orders"
        )

    return render(
        request,
        "management/order_edit.html",
        {
            "order": order,
        },
    )


# =========================================================
# CUSTOMERS
# =========================================================

@store_owner_required
def customer_list(request):

    customers = CustomerProfile.objects.select_related(
        "user"
    ).order_by("-user__date_joined")

    return render(
        request,
        "management/customers.html",
        {
            "customers": customers,
        },
    )


@store_owner_required
def customer_detail(request, customer_id):

    customer = get_object_or_404(
        CustomerProfile.objects.select_related("user"),
        id=customer_id,
    )

    orders = Order.objects.filter(
        customer=customer.user
    ).prefetch_related(
        "items"
    ).order_by("-created_at")

    return render(
        request,
        "management/customer_detail.html",
        {
            "customer": customer,
            "orders": orders,
        },
    )


# =========================================================
# CATEGORIES
# =========================================================

@store_owner_required
def category_list(request):

    categories = Category.objects.all().order_by(
        "name"
    )

    return render(
        request,
        "management/categories.html",
        {
            "categories": categories,
        },
    )


@store_owner_required
def category_create(request):

    if request.method == "POST":

        form = CategoryForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect(
                "management:categories"
            )

    else:

        form = CategoryForm()

    return render(
        request,
        "management/category_form.html",
        {
            "form": form,
        },
    )


@store_owner_required
def category_edit(request, category_id):

    category = get_object_or_404(
        Category,
        id=category_id,
    )

    if request.method == "POST":

        form = CategoryForm(
            request.POST,
            instance=category,
        )

        if form.is_valid():

            form.save()

            return redirect(
                "management:categories"
            )

    else:

        form = CategoryForm(
            instance=category,
        )

    return render(
        request,
        "management/category_form.html",
        {
            "form": form,
            "editing": True,
            "category": category,
        },
    )