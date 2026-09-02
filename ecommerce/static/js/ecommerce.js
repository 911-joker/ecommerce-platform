document.addEventListener("DOMContentLoaded", function () {

    /* =========================================================
       MOBILE MENU
    ========================================================= */

    const mobileMenuToggle = document.getElementById(
        "mobile-menu-toggle"
    );

    const mobileMenu = document.getElementById(
        "mobile-menu"
    );


    if (mobileMenuToggle && mobileMenu) {

        mobileMenuToggle.addEventListener("click", function () {

            const isOpen =
                mobileMenu.classList.contains("is-open");


            if (isOpen) {

                mobileMenu.classList.remove("is-open");

                mobileMenuToggle.classList.remove("is-open");

                mobileMenuToggle.setAttribute(
                    "aria-expanded",
                    "false"
                );

                mobileMenu.setAttribute(
                    "aria-hidden",
                    "true"
                );

                mobileMenuToggle.setAttribute(
                    "aria-label",
                    "Open menu"
                );

            } else {

                mobileMenu.classList.add("is-open");

                mobileMenuToggle.classList.add("is-open");

                mobileMenuToggle.setAttribute(
                    "aria-expanded",
                    "true"
                );

                mobileMenu.setAttribute(
                    "aria-hidden",
                    "false"
                );

                mobileMenuToggle.setAttribute(
                    "aria-label",
                    "Close menu"
                );

            }

        });

    }


    /* =========================================================
       DESKTOP SEARCH
    ========================================================= */

    const desktopSearch =
        document.getElementById("desktop-search");

    const desktopSearchToggle =
        document.getElementById("desktop-search-toggle");

    const desktopSearchInput =
        document.getElementById("desktop-search-input");


    if (
        desktopSearch &&
        desktopSearchToggle
    ) {

        desktopSearchToggle.addEventListener(
            "click",
            function (event) {

                event.preventDefault();

                const isOpen =
                    desktopSearch.classList.contains(
                        "is-open"
                    );


                if (isOpen) {

                    desktopSearch.classList.remove(
                        "is-open"
                    );

                    desktopSearchToggle.setAttribute(
                        "aria-expanded",
                        "false"
                    );

                    if (desktopSearchInput) {

                        desktopSearchInput.blur();

                    }

                } else {

                    desktopSearch.classList.add(
                        "is-open"
                    );

                    desktopSearchToggle.setAttribute(
                        "aria-expanded",
                        "true"
                    );

                    if (desktopSearchInput) {

                        setTimeout(function () {

                            desktopSearchInput.focus();

                        }, 300);

                    }

                }

            }
        );

    }


    /* =========================================================
       CLOSE DESKTOP SEARCH WHEN CLICKING OUTSIDE
    ========================================================= */

    document.addEventListener(
        "click",
        function (event) {

            if (!desktopSearch) {
                return;
            }


            if (
                desktopSearch.classList.contains(
                    "is-open"
                ) &&
                !desktopSearch.contains(event.target)
            ) {

                desktopSearch.classList.remove(
                    "is-open"
                );

                if (desktopSearchToggle) {

                    desktopSearchToggle.setAttribute(
                        "aria-expanded",
                        "false"
                    );

                }

            }

        }
    );


    /* =========================================================
       DESKTOP SEARCH - ESCAPE KEY
    ========================================================= */

    document.addEventListener(
        "keydown",
        function (event) {

            if (event.key !== "Escape") {
                return;
            }


            if (
                desktopSearch &&
                desktopSearch.classList.contains(
                    "is-open"
                )
            ) {

                desktopSearch.classList.remove(
                    "is-open"
                );

                if (desktopSearchToggle) {

                    desktopSearchToggle.setAttribute(
                        "aria-expanded",
                        "false"
                    );

                }

            }

        }
    );


    /* =========================================================
       MOBILE SEARCH
    ========================================================= */

    const mobileSearchToggle =
        document.getElementById(
            "mobile-search-toggle"
        );

    const mobileSearchPanel =
        document.getElementById(
            "mobile-search-panel"
        );

    const mobileSearchInput =
        document.getElementById(
            "mobile-search-input"
        );


    if (
        mobileSearchToggle &&
        mobileSearchPanel
    ) {

        mobileSearchToggle.addEventListener(
            "click",
            function (event) {

                event.preventDefault();

                const isOpen =
                    mobileSearchPanel.classList.contains(
                        "is-open"
                    );


                if (isOpen) {

                    mobileSearchPanel.classList.remove(
                        "is-open"
                    );

                    mobileSearchToggle.setAttribute(
                        "aria-expanded",
                        "false"
                    );

                } else {

                    mobileSearchPanel.classList.add(
                        "is-open"
                    );

                    mobileSearchToggle.setAttribute(
                        "aria-expanded",
                        "true"
                    );


                    /*
                     * Close the hamburger menu when
                     * opening search.
                     */

                    if (mobileMenu) {

                        mobileMenu.classList.remove(
                            "is-open"
                        );

                    }

                    if (mobileMenuToggle) {

                        mobileMenuToggle.classList.remove(
                            "is-open"
                        );

                        mobileMenuToggle.setAttribute(
                            "aria-expanded",
                            "false"
                        );

                        mobileMenuToggle.setAttribute(
                            "aria-label",
                            "Open menu"
                        );

                    }


                    /*
                     * Focus the search field after
                     * the panel becomes visible.
                     */

                    if (mobileSearchInput) {

                        setTimeout(function () {

                            mobileSearchInput.focus();

                        }, 100);

                    }

                }

            }
        );

    }


    /* =========================================================
       CLOSE MOBILE SEARCH WITH ESCAPE
    ========================================================= */

    document.addEventListener(
        "keydown",
        function (event) {

            if (event.key !== "Escape") {
                return;
            }


            if (
                mobileSearchPanel &&
                mobileSearchPanel.classList.contains(
                    "is-open"
                )
            ) {

                mobileSearchPanel.classList.remove(
                    "is-open"
                );

                if (mobileSearchToggle) {

                    mobileSearchToggle.setAttribute(
                        "aria-expanded",
                        "false"
                    );

                }

            }

        }
    );


    /* =========================================================
       PRODUCT VARIANT SYSTEM
    ========================================================= */

    const variantForm =
        document.getElementById(
            "variant-form"
        );


    /*
     * IMPORTANT:
     *
     * Do NOT return from the entire script here.
     *
     * The navigation/search system above must continue
     * working on pages that don't contain a variant form.
     */

    if (!variantForm) {
        return;
    }


    /* =========================================================
       PRODUCT ELEMENTS
    ========================================================= */

    const productImage =
        document.getElementById(
            "product-main-image"
        );

    const colorInputs =
        variantForm.querySelectorAll(
            'input[name="color_choice"]'
        );

    const sizeOptions =
        variantForm.querySelectorAll(
            ".size-option"
        );

    const sizeInputs =
        variantForm.querySelectorAll(
            'input[name="size_choice"]'
        );

    const selectedVariantInput =
        document.getElementById(
            "selected-variant"
        );

    const stockText =
        document.getElementById(
            "variant-stock"
        );

    const stockDot =
        document.getElementById(
            "stock-dot"
        );

    const addButton =
        document.getElementById(
            "add-to-cart-button"
        );


    /* =========================================================
       SAFETY CHECK
    ========================================================= */

    if (
        !selectedVariantInput ||
        !stockText ||
        !stockDot ||
        !addButton
    ) {

        return;

    }


    /* =========================================================
       RESET SELECTED VARIANT
    ========================================================= */

    function resetVariant() {

        selectedVariantInput.value = "";

        stockText.textContent =
            "Select a size";

        stockDot.classList.remove(
            "out"
        );

        addButton.disabled = true;

        addButton.textContent =
            "Select Size";

    }


    /* =========================================================
       UPDATE PRODUCT IMAGE
    ========================================================= */

    function updateProductImage() {

        const selectedColor =
            variantForm.querySelector(
                'input[name="color_choice"]:checked'
            );


        if (
            !selectedColor ||
            !productImage
        ) {

            return;

        }


        const imageUrl =
            selectedColor.dataset.image;


        if (imageUrl) {

            productImage.src =
                imageUrl;

            productImage.alt =
                `${selectedColor.value} ${document.title
                    .replace(" | STORE", "")}`;

        }

    }


    /* =========================================================
       UPDATE AVAILABLE SIZES
    ========================================================= */

    function updateSizes() {

        const selectedColor =
            variantForm.querySelector(
                'input[name="color_choice"]:checked'
            );


        if (!selectedColor) {

            return;

        }


        const selectedColorValue =
            selectedColor.value;


        /*
         * Update product image.
         */

        updateProductImage();


        /*
         * Clear previous size.
         */

        sizeInputs.forEach(
            function (input) {

                input.checked = false;

            }
        );


        /*
         * Reset variant.
         */

        resetVariant();


        /*
         * Display only sizes belonging
         * to selected color.
         */

        sizeOptions.forEach(
            function (option) {

                const optionColor =
                    option.dataset.color;

                const input =
                    option.querySelector(
                        'input[name="size_choice"]'
                    );


                if (!input) {

                    return;

                }


                if (
                    optionColor ===
                    selectedColorValue
                ) {

                    option.style.display =
                        "inline-flex";

                    input.disabled = false;

                } else {

                    option.style.display =
                        "none";

                    input.disabled = true;

                    input.checked = false;

                }

            }
        );

    }


    /* =========================================================
       UPDATE SELECTED VARIANT
    ========================================================= */

    function updateVariant() {

        const selectedSize =
            variantForm.querySelector(
                'input[name="size_choice"]:checked'
            );


        if (!selectedSize) {

            resetVariant();

            return;

        }


        /*
         * ProductVariant ID.
         */

        const variantId =
            selectedSize.value;


        selectedVariantInput.value =
            variantId;


        /*
         * Stock.
         */

        const stock =
            Number(
                selectedSize.dataset.stock
            );


        if (stock > 0) {

            stockText.textContent =
                `${stock} available`;

            stockDot.classList.remove(
                "out"
            );

            addButton.disabled = false;

            addButton.textContent =
                "Add to Cart";

        } else {

            stockText.textContent =
                "Out of stock";

            stockDot.classList.add(
                "out"
            );

            addButton.disabled = true;

            addButton.textContent =
                "Out of Stock";

        }

    }


    /* =========================================================
       COLOR EVENTS
    ========================================================= */

    colorInputs.forEach(
        function (input) {

            input.addEventListener(
                "change",
                updateSizes
            );

        }
    );


    /* =========================================================
       SIZE EVENTS
    ========================================================= */

    sizeInputs.forEach(
        function (input) {

            input.addEventListener(
                "change",
                updateVariant
            );

        }
    );


    /* =========================================================
       INITIALISE PRODUCT PAGE
    ========================================================= */

    updateSizes();

});


/* =========================================================
   PROFILE DELIVERY MODAL
========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    const editDeliveryButton =
        document.getElementById(
            "edit-delivery-button"
        );

    const deliveryModalOverlay =
        document.getElementById(
            "delivery-modal-overlay"
        );

    const deliveryModalClose =
        document.getElementById(
            "delivery-modal-close"
        );


    /*
     * Stop here on pages that do not contain
     * the delivery popup.
     */

    if (
        !editDeliveryButton ||
        !deliveryModalOverlay
    ) {
        return;
    }


    /* =====================================================
       OPEN POPUP
    ===================================================== */

    editDeliveryButton.addEventListener(
        "click",
        function () {

            deliveryModalOverlay.classList.remove(
                "is-hidden"
            );

            deliveryModalOverlay.setAttribute(
                "aria-hidden",
                "false"
            );

            document.body.classList.add(
                "modal-open"
            );

        }
    );


    /* =====================================================
       CLOSE POPUP
    ===================================================== */

    function closeDeliveryModal() {

        deliveryModalOverlay.classList.add(
            "is-hidden"
        );

        deliveryModalOverlay.setAttribute(
            "aria-hidden",
            "true"
        );

        document.body.classList.remove(
            "modal-open"
        );

    }


    /* =====================================================
       CLOSE BUTTON
    ===================================================== */

    if (deliveryModalClose) {

        deliveryModalClose.addEventListener(
            "click",
            closeDeliveryModal
        );

    }


    /* =====================================================
       CLICK OUTSIDE POPUP
    ===================================================== */

    deliveryModalOverlay.addEventListener(
        "click",
        function (event) {

            if (
                event.target ===
                deliveryModalOverlay
            ) {

                closeDeliveryModal();

            }

        }
    );


    /* =====================================================
       ESCAPE KEY
    ===================================================== */

    document.addEventListener(
        "keydown",
        function (event) {

            if (
                event.key === "Escape" &&
                !deliveryModalOverlay.classList.contains(
                    "is-hidden"
                )
            ) {

                closeDeliveryModal();

            }

        }
    );

});


/* =========================================================
   MANAGEMENT - PRODUCT VARIANTS
========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    const addVariantButton =
        document.getElementById("add-variant-button");

    const variantContainer =
        document.getElementById("variant-forms");

    const emptyVariantTemplate =
        document.getElementById("empty-variant-form");

    const totalForms =
        document.getElementById("id_variants-TOTAL_FORMS");


    /*
     * This script only runs on the
     * management product form.
     */

    if (
        !addVariantButton ||
        !variantContainer ||
        !emptyVariantTemplate ||
        !totalForms
    ) {
        return;
    }


    /* =====================================================
       UPDATE VARIANT NUMBERS
    ===================================================== */

    function updateVariantNumbers() {

        const variants =
            variantContainer.querySelectorAll(
                ".variant-form"
            );


        variants.forEach(function (variant, index) {

            const number =
                variant.querySelector(
                    ".variant-number"
                );


            if (number) {

                number.textContent =
                    index + 1;

            }

        });

    }


    /* =====================================================
       ADD VARIANT
    ===================================================== */

    addVariantButton.addEventListener(
        "click",
        function () {

            const formIndex =
                parseInt(
                    totalForms.value,
                    10
                );


            const newVariant =
                emptyVariantTemplate.innerHTML.replace(
                    /__prefix__/g,
                    formIndex
                );


            variantContainer.insertAdjacentHTML(
                "beforeend",
                newVariant
            );


            totalForms.value =
                formIndex + 1;


            updateVariantNumbers();

        }
    );


    /* =====================================================
       INITIALISE
    ===================================================== */

    updateVariantNumbers();

});