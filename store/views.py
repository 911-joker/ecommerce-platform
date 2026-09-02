import requests

from django.conf import settings
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .cart import Cart
from .forms import RegisterForm, CustomerProfileForm
from .models import (
    Product,
    ProductVariant,
    Order,
    OrderItem,
    ShopPage,
    CustomerProfile,
    Category,
)


# =========================================================
# ADD TO CART
# =========================================================

def add_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
    )

    variant_id = request.POST.get("variant_id")


    # -----------------------------------------------------
    # PRODUCT WITH VARIANTS
    # -----------------------------------------------------

    if product.variants.exists():

        if not variant_id:

            messages.error(
                request,
                "Please select a size and color.",
            )

            return redirect(product.url)


        variant = get_object_or_404(
            ProductVariant,
            id=variant_id,
            product=product,
        )


        if variant.stock <= 0:

            messages.error(
                request,
                f"{variant.color} / {variant.size} is currently out of stock.",
            )

            return redirect(product.url)


        cart = Cart(request)

        current_quantity = 0


        for item in cart:

            if item.get("variant_id") == variant.id:

                current_quantity = item["quantity"]

                break


        if current_quantity >= variant.stock:

            messages.warning(
                request,
                f"Only {variant.stock} units of "
                f"{variant.color} / {variant.size} are available.",
            )

        else:

            cart.add(
                product,
                quantity=1,
                variant=variant,
            )

            messages.success(
                request,
                f"{product.title} "
                f"({variant.color} / {variant.size}) "
                f"was added to your cart.",
            )


        return redirect("store:cart")


    # -----------------------------------------------------
    # NORMAL PRODUCT WITHOUT VARIANTS
    # -----------------------------------------------------
    #
    # Your current Product model uses ProductVariant for
    # inventory. Therefore this branch is retained safely
    # but does not assume Product has stock/in_stock fields.
    #

    messages.error(
        request,
        f"{product.title} has no available variants.",
    )

    return redirect(product.url)


# =========================================================
# CART
# =========================================================

def cart_detail(request):

    cart = Cart(request)

    return render(
        request,
        "store/cart.html",
        {
            "cart": cart,
        },
    )


# =========================================================
# REMOVE FROM CART
# =========================================================

def remove_from_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
    )

    variant_id = request.POST.get("variant_id")

    variant = None


    if variant_id:

        variant = get_object_or_404(
            ProductVariant,
            id=variant_id,
            product=product,
        )


    cart = Cart(request)

    cart.remove(
        product,
        variant=variant,
    )


    return redirect("store:cart")


# =========================================================
# UPDATE CART
# =========================================================

def update_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
    )

    variant_id = request.POST.get("variant_id")

    variant = None


    if variant_id:

        variant = get_object_or_404(
            ProductVariant,
            id=variant_id,
            product=product,
        )


    try:

        quantity = int(
            request.POST.get(
                "quantity",
                1,
            )
        )

    except (TypeError, ValueError):

        quantity = 1


    cart = Cart(request)


    # -----------------------------------------------------
    # VARIANT PRODUCT
    # -----------------------------------------------------

    if variant:

        if quantity <= 0:

            cart.remove(
                product,
                variant=variant,
            )

            messages.success(
                request,
                f"{product.title} "
                f"({variant.color} / {variant.size}) "
                f"was removed from your cart.",
            )

        elif variant.stock <= 0:

            messages.error(
                request,
                f"{variant.color} / {variant.size} "
                f"is currently out of stock.",
            )

        elif quantity > variant.stock:

            messages.warning(
                request,
                f"Only {variant.stock} units of "
                f"{variant.color} / {variant.size} are available.",
            )

        else:

            cart.update(
                product,
                quantity,
                variant=variant,
            )

            messages.success(
                request,
                f"{product.title} "
                f"({variant.color} / {variant.size}) "
                f"quantity updated.",
            )


        return redirect("store:cart")


    # -----------------------------------------------------
    # NO VARIANT
    # -----------------------------------------------------

    if quantity <= 0:

        cart.remove(product)

        messages.success(
            request,
            f"{product.title} was removed from your cart.",
        )

    else:

        messages.error(
            request,
            f"{product.title} does not have a valid variant.",
        )


    return redirect("store:cart")


# =========================================================
# PAYSTACK — INITIALIZE TRANSACTION
# =========================================================

def initialize_paystack_transaction(
    email,
    amount,
    reference,
    callback_url,
):

    url = f"{settings.PAYSTACK_BASE_URL}/transaction/initialize"

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "email": email,
        "amount": amount,
        "reference": reference,
        "callback_url": callback_url,
    }

    response = requests.post(
        url,
        headers=headers,
        json=data,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


# =========================================================
# PAYSTACK — VERIFY TRANSACTION
# =========================================================

def verify_paystack_transaction(reference):

    url = (
        f"{settings.PAYSTACK_BASE_URL}"
        f"/transaction/verify/{reference}"
    )

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


# =========================================================
# PAYSTACK — START PAYMENT
# =========================================================

@login_required
def start_payment(request):

    if request.method != "POST":
        return redirect("store:checkout")


    cart = Cart(request)


    if len(cart) == 0:
        return redirect("store:cart")


    profile, created = CustomerProfile.objects.get_or_create(
        user=request.user
    )


    # -----------------------------------------------------
    # CHECK STOCK BEFORE STARTING PAYMENT
    # -----------------------------------------------------

    for item in cart:

        product = item["product"]

        variant = item["variant"]

        quantity = item["quantity"]


        if not variant:

            messages.error(
                request,
                f"{product.title} no longer has a valid variant.",
            )

            return redirect("store:cart")


        variant = ProductVariant.objects.get(
            id=variant.id,
            product=product,
        )


        if variant.stock < quantity:

            messages.error(
                request,
                f"Not enough stock for "
                f"{product.title} "
                f"({variant.color} / {variant.size}).",
            )

            return redirect("store:cart")


    # -----------------------------------------------------
    # CREATE UNIQUE PAYMENT REFERENCE
    # -----------------------------------------------------

    import uuid

    reference = (
        f"STORE-{request.user.id}-"
        f"{uuid.uuid4().hex[:16].upper()}"
    )


    # -----------------------------------------------------
    # AMOUNT
    #
    # Paystack expects the amount in the smallest
    # currency unit.
    #
    # ₦30,000.00 → 3000000 kobo
    # -----------------------------------------------------

    amount = int(
        cart.get_total_price() * 100
    )


    # -----------------------------------------------------
    # CALLBACK URL
    # -----------------------------------------------------

    callback_url = request.build_absolute_uri(
        "/payment/verify/"
    )


    # -----------------------------------------------------
    # INITIALIZE PAYSTACK
    # -----------------------------------------------------

    try:

        payment_response = initialize_paystack_transaction(

            email=request.user.email,

            amount=amount,

            reference=reference,

            callback_url=callback_url,

        )

    except requests.RequestException:

        messages.error(
            request,
            "We could not connect to the payment service. "
            "Please try again.",
        )

        return redirect("store:checkout")


    # -----------------------------------------------------
    # CHECK PAYSTACK RESPONSE
    # -----------------------------------------------------

    if not payment_response.get("status"):

        messages.error(
            request,
            "Unable to initialize payment. "
            "Please try again.",
        )

        return redirect("store:checkout")


    payment_data = payment_response.get(
        "data",
        {}
    )


    authorization_url = payment_data.get(
        "authorization_url"
    )


    if not authorization_url:

        messages.error(
            request,
            "Payment initialization failed. "
            "Please try again.",
        )

        return redirect("store:checkout")


    # -----------------------------------------------------
    # STORE REFERENCE IN SESSION
    # -----------------------------------------------------

    request.session["paystack_reference"] = reference


    # -----------------------------------------------------
    # REDIRECT TO PAYSTACK
    # -----------------------------------------------------

    return redirect(
        authorization_url
    )


# =========================================================
# PAYSTACK — VERIFY PAYMENT
# =========================================================

@login_required
def verify_payment(request):

    reference = request.GET.get("reference")


    if not reference:

        messages.error(
            request,
            "No payment reference was provided.",
        )

        return redirect("store:checkout")


    # -----------------------------------------------------
    # VERIFY TRANSACTION WITH PAYSTACK
    # -----------------------------------------------------

    try:

        payment_response = verify_paystack_transaction(
            reference
        )

    except requests.RequestException:

        messages.error(
            request,
            "We could not verify your payment. "
            "Please contact support if money was deducted.",
        )

        return redirect("store:checkout")


    # -----------------------------------------------------
    # CHECK PAYSTACK RESPONSE
    # -----------------------------------------------------

    if not payment_response.get("status"):

        messages.error(
            request,
            "Payment verification failed.",
        )

        return redirect("store:checkout")


    payment_data = payment_response.get(
        "data",
        {}
    )


    # -----------------------------------------------------
    # PAYMENT MUST BE SUCCESSFUL
    # -----------------------------------------------------

    if payment_data.get("status") != "success":

        messages.error(
            request,
            "Your payment was not successful.",
        )

        return redirect("store:checkout")


    # -----------------------------------------------------
    # REFERENCE MUST MATCH
    # -----------------------------------------------------

    if payment_data.get("reference") != reference:

        messages.error(
            request,
            "Payment reference could not be verified.",
        )

        return redirect("store:checkout")


    # -----------------------------------------------------
    # REFERENCE MUST BELONG TO THIS SESSION
    # -----------------------------------------------------

    session_reference = request.session.get(
        "paystack_reference"
    )


    if session_reference != reference:

        messages.error(
            request,
            "This payment session is invalid.",
        )

        return redirect("store:checkout")


    # -----------------------------------------------------
    # GET CART
    # -----------------------------------------------------

    cart = Cart(request)


    if len(cart) == 0:

        messages.error(
            request,
            "Your cart is empty.",
        )

        return redirect("store:cart")


    # -----------------------------------------------------
    # VERIFY AMOUNT
    #
    # Paystack returns the amount in kobo.
    # Our cart total is in naira.
    # -----------------------------------------------------

    expected_amount = int(
        cart.get_total_price() * 100
    )


    paid_amount = int(
        payment_data.get(
            "amount",
            0
        )
    )


    if paid_amount != expected_amount:

        messages.error(
            request,
            "The payment amount could not be verified.",
        )

        return redirect("store:checkout")


    # -----------------------------------------------------
    # CREATE ORDER + DEDUCT STOCK
    # -----------------------------------------------------

    profile, created = CustomerProfile.objects.get_or_create(
        user=request.user
    )


    with transaction.atomic():

        # ---------------------------------------------
        # CHECK STOCK AGAIN
        # ---------------------------------------------

        for item in cart:

            product = item["product"]

            variant = item["variant"]

            quantity = item["quantity"]


            if not variant:

                messages.error(
                    request,
                    f"{product.title} no longer has a valid variant.",
                )

                return redirect("store:cart")


            variant = ProductVariant.objects.select_for_update().get(
                id=variant.id,
                product=product,
            )


            if variant.stock < quantity:

                messages.error(
                    request,
                    f"Not enough stock for "
                    f"{product.title} "
                    f"({variant.color} / {variant.size}).",
                )

                return redirect("store:cart")


        # ---------------------------------------------
        # CREATE PAID ORDER
        # ---------------------------------------------

        order = Order.objects.create(

            customer=request.user,

            first_name=request.user.first_name,

            last_name=request.user.last_name,

            email=request.user.email,

            phone=profile.phone,

            address=profile.address,

            city=profile.city,

            state=profile.state,

            total=cart.get_total_price(),

            paystack_reference=reference,

            status="paid",

        )


        # ---------------------------------------------
        # CREATE ORDER ITEMS + REDUCE STOCK
        # ---------------------------------------------

        for item in cart:

            product = item["product"]

            variant = item["variant"]

            quantity = item["quantity"]


            variant = ProductVariant.objects.select_for_update().get(
                id=variant.id,
                product=product,
            )


            OrderItem.objects.create(

                order=order,

                product=product,

                variant=variant,

                price=item["price"],

                quantity=quantity,

            )


            variant.stock -= quantity

            variant.save(
                update_fields=[
                    "stock"
                ]
            )


    # -----------------------------------------------------
    # CLEAR CART
    # -----------------------------------------------------

    cart.clear()


    # -----------------------------------------------------
    # REMOVE PAYMENT REFERENCE FROM SESSION
    # -----------------------------------------------------

    request.session.pop(
        "paystack_reference",
        None,
    )


    # -----------------------------------------------------
    # ORDER CONFIRMATION
    # -----------------------------------------------------

    return redirect(
        "store:order_success",
        order_id=order.id,
    )


# =========================================================
# CHECKOUT
# =========================================================

@login_required
def checkout(request):

    cart = Cart(request)

    if len(cart) == 0:
        return redirect("store:cart")

    profile, created = CustomerProfile.objects.get_or_create(
        user=request.user
    )

    return render(
        request,
        "store/checkout.html",
        {
            "cart": cart,
            "profile": profile,
        },
    )


# =========================================================
# ORDER SUCCESS
# =========================================================

@login_required
def order_success(request, order_id):

    order = get_object_or_404(

        Order,

        id=order_id,

        customer=request.user,

    )


    return render(

        request,

        "store/order_success.html",

        {
            "order": order,
        },

    )


# =========================================================
# ORDER HISTORY
# =========================================================

@login_required
def order_history(request):

    orders = request.user.orders.all()

    shop_page = ShopPage.objects.live().first()


    return render(

        request,

        "store/order_history.html",

        {
            "orders": orders,

            "shop_page": shop_page,
        },

    )


# =========================================================
# REORDER
# =========================================================

@login_required
def reorder(request, order_id):

    order = get_object_or_404(

        Order,

        id=order_id,

        customer=request.user,

    )


    cart = Cart(request)


    for item in order.items.all():

        # -------------------------------------------------
        # ONLY READD ITEMS WHOSE VARIANT STILL EXISTS
        # -------------------------------------------------

        if item.variant:

            cart.add(

                item.product,

                quantity=item.quantity,

                variant=item.variant,

            )


    return redirect("store:cart")


# =========================================================
# REGISTER
# =========================================================

def register(request):

    if request.user.is_authenticated:

        return redirect(
            "accounts:profile"
        )


    if request.method == "POST":

        form = RegisterForm(
            request.POST
        )


        if form.is_valid():

            user = form.save()


            CustomerProfile.objects.create(
                user=user,
            )


            login(
                request,
                user,
            )


            return redirect(
                "accounts:profile"
            )


    else:

        form = RegisterForm()


    return render(

        request,

        "store/register.html",

        {
            "form": form,
        },

    )


# =========================================================
# PROFILE
# =========================================================

@login_required
def profile(request):

    profile, created = CustomerProfile.objects.get_or_create(
        user=request.user
    )

    shop_page = ShopPage.objects.live().first()

    profile_complete = all([
        request.user.first_name,
        request.user.last_name,
        request.user.email,
        profile.phone,
        profile.address,
        profile.city,
        profile.state,
    ])

    # =====================================================
    # POST — UPDATE DELIVERY INFORMATION
    # =====================================================

    if request.method == "POST":

        form = CustomerProfileForm(
            request.POST,
            instance=profile,
        )

        if form.is_valid():

            form.save()

            return redirect(
                "accounts:profile"
            )

    # =====================================================
    # GET — DISPLAY ACCOUNT
    # =====================================================

    else:

        form = CustomerProfileForm(
            instance=profile
        )

    return render(
        request,
        "store/profile.html",
        {
            "profile": profile,
            "form": form,
            "shop_page": shop_page,
            "profile_complete": profile_complete,
        },
    )


# =========================================================
# PREPARE PRODUCTS FOR SHOP
# =========================================================

def prepare_shop_products(products):

    products = products.prefetch_related("variants")

    for product in products:

        variants = list(product.variants.all())

        # -------------------------------------------------
        # PRODUCT HAS VARIANTS
        # -------------------------------------------------

        if variants:

            # First variant = default variant
            default_variant = variants[0]

            product.default_variant = default_variant

            # Stock shown on the shop card belongs ONLY
            # to the default variant.
            product.is_available = (
                default_variant.stock > 0
            )

        # -------------------------------------------------
        # PRODUCT HAS NO VARIANTS
        # -------------------------------------------------

        else:

            product.default_variant = None

            product.is_available = (
                product.in_stock
                and product.stock > 0
            )

    return products


# =========================================================
# ALL PRODUCTS
# =========================================================

def shop(request):

    products = (
        Product.objects
        .live()
        .specific()
    )


    products = prepare_shop_products(
        products
    )


    return render(

        request,

        "store/shop_page.html",

        {
            "products": products,

            "page_title": "All",
        },

    )


# =========================================================
# CATEGORY SHOP
# =========================================================

def category_shop(request, slug):

    category = get_object_or_404(

        Category,

        slug=slug,

    )


    products = (
        Product.objects
        .live()
        .specific()
        .filter(
            category=category,
        )
    )


    products = prepare_shop_products(
        products
    )


    return render(

        request,

        "store/shop_page.html",

        {
            "products": products,

            "page_title": category.name,

            "category": category,
        },

    )


# =========================================================
# SEARCH
# =========================================================

def search(request):

    query = request.GET.get(
        "q",
        "",
    ).strip()


    products = (
        Product.objects
        .live()
        .specific()
        .prefetch_related(
            "variants"
        )
    )


    # -----------------------------------------------------
    # SEARCH QUERY
    # -----------------------------------------------------

    if query:

        products = products.filter(

            Q(
                title__icontains=query
            )

            |

            Q(
                description__icontains=query
            )

            |

            Q(
                category__name__icontains=query
            )

            |

            Q(
                variants__color__icontains=query
            )

            |

            Q(
                variants__size__icontains=query
            )

        ).distinct()


    # -----------------------------------------------------
    # PREPARE AVAILABILITY
    # -----------------------------------------------------

    products = prepare_shop_products(
        products
    )


    # -----------------------------------------------------
    # BUILD SEARCH RESULTS
    # -----------------------------------------------------

    search_results = []


    for product in products:

        variant = (
            product.variants
            .select_related(
                "image"
            )
            .filter(
                image__isnull=False
            )
            .first()
        )


        image = (
            variant.image
            if variant
            else None
        )


        search_results.append({

            "product": product,

            "image": image,

        })


    # -----------------------------------------------------
    # RENDER SEARCH PAGE
    # -----------------------------------------------------

    return render(

        request,

        "store/search.html",

        {
            "query": query,

            "products": products,

            "search_results": search_results,
        },

    )