from django.urls import path

from . import views


app_name = "management"


urlpatterns = [

    path(
        "",
        views.dashboard,
        name="dashboard",
    ),

    # PRODUCTS

    path(
        "products/",
        views.product_list,
        name="products",
    ),

    path(
        "products/add/",
        views.product_create,
        name="product_create",
    ),

    path(
        "products/<int:product_id>/edit/",
        views.product_edit,
        name="product_edit",
    ),

    # ORDERS

    path(
        "orders/",
        views.order_list,
        name="orders",
    ),

    path(
        "orders/<int:order_id>/edit/",
        views.order_edit,
        name="order_edit",
    ),

    # CUSTOMERS

    path(
        "customers/",
        views.customer_list,
        name="customers",
    ),

    path(
        "customers/<int:customer_id>/",
        views.customer_detail,
        name="customer_detail",
    ),

    # CATEGORIES

    path(
        "categories/",
        views.category_list,
        name="categories",
    ),

    path(
        "categories/add/",
        views.category_create,
        name="category_create",
    ),

    path(
        "categories/<int:category_id>/edit/",
        views.category_edit,
        name="category_edit",
    ),

]