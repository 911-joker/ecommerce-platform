from django.urls import path

from . import views


app_name = "store"


urlpatterns = [
    path(
        "cart/",
        views.cart_detail,
        name="cart",
    ),

    path(
        "cart/add/<int:product_id>/",
        views.add_to_cart,
        name="cart_add",
    ),

    path(
        "cart/remove/<int:product_id>/",
        views.remove_from_cart,
        name="cart_remove",
    ),

    path(
        "cart/update/<int:product_id>/",
        views.update_cart,
        name="cart_update",
    ),

    path(
        "checkout/",
        views.checkout,
        name="checkout",
    ),

    path(
        "payment/start/",
        views.start_payment,
        name="payment_start",
    ),    

    path(
        "payment/verify/",
        views.verify_payment,
        name="payment_verify",
    ),

    path(
        "order/success/<int:order_id>/",
        views.order_success,
        name="order_success",
    ),

    path(
        "orders/",
        views.order_history,
        name="order_history",
    ),

    path(
        "orders/<int:order_id>/reorder/",
        views.reorder,
        name="reorder",
    ),

    path(
        "shop/", 
        views.shop, 
        name="shop"
    ),

    path(
        "men/",
        views.category_shop,
        {"slug": "men"},
        name="men",
    ),

    path(
        "women/",
        views.category_shop,
        {"slug": "women"},
        name="women",
    ),

    path(
        "search/",
        views.search,
        name="search",
    ),

]