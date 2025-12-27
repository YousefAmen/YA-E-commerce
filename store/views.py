from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .models import *
from django.urls import reverse

from members.models import Merchant, Customer, User
from .forms import (
    Contact_Us_Form,
    ProductImageForm,
    InventoryForm,
    AddCategoriesForm,
    DaynamicProductForm,
)
from django.contrib import messages
from django.db.models import Q
from payment.models import OrderItem, Order
from django.db.models import Count, Sum
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import transaction
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect

# MODEL_MAPPING = {
#     "phone": Phone,
#     "shoe": Shoe,
#     "laptop": Laptop,
#     "tablet": Tablet,
#     "headphone": Headphone,
#     "clothing": Clothing,
#     "watch": Watch,
#     "sportequipment": SportEquipment,
#     "book": Book,
# }


def home(request):
    context = {
        "products": Product.objects.all(),
        "categories": Category.objects.all(),
    }

    return render(request, "store/index.html", context)


def about(request):
    return render(request, "store/about.html")


def product_details(request, slug, id):

    product = Product.objects.get(slug=slug, id=id)
    if not product:
        messages.error(request, "Product not found.")
        return redirect("home")

    related_products = Product.objects.filter(category=product.category).exclude(
        slug=product.slug
    )

    inventory = []
    for i in range(1, product.inventory.quantity + 1):
        inventory.append(i)
    session_key = f"viewed_product_{product.id}"

    # views codebase
    if not request.session.get(session_key):
        request.session[session_key] = True
        product.views_number += 1
        product.save()
        if request.user.is_authenticated:
            product.views.add(request.user)

        request.session[session_key] = True
        request.session.modified = True
    context = {
        "product": product,
        "inventory": inventory,
        "related_products": related_products,
    }
    return render(request, "store/product_details.html", context)


def all_categories(requset):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {"categories": categories, "products": products}
    return render(requset, "store/all_categories.html", context)


def category(request, cat):
    try:
        products = Product.objects.filter(category__name=cat)
        return render(
            request, "store/category.html", {"products": products, "category": cat}
        )
    except Category.DoesNotExist:
        messages.info(request, "This Category Dose Not Exists...")
        return redirect("/")


def discount_products(request):
    products = Product.objects.filter(discount__gt=0)
    context = {"products": products}
    return render(request, "store/offers.html", context)


def get_user(request, slug, id):
    try:
        user = User.objects.get(slug=slug, id=id)
    except User.DoesNotExist:
        messages.error(
            request, "sorry,there's a problem please re-registering a agine."
        )
    if user.role == "merchant":
        merchant = Merchant.objects.get(user=user)
    else:
        customer = Customer.objects.get(user=user)
    if merchant:
        return merchant
    return customer


# choosing product category function
@csrf_protect
def choosing_product_category(request):
    # display all main category
    # get the choice category from the merchant
    # send the category to the choosing_sub_category

    if request.method == "POST":
        category_slug = request.POST["category_slug"]
        if not category_slug:
            messages.info(request, "please select a category.")
            return render(
                request, "store/choosing_category.html", {"categories": categories}
            )
        categories = Category.objects.filter(parent__isnull=True)

        return redirect("choosing_sub_category", category_slug=category_slug)
    categories = Category.objects.filter(parent__isnull=True)

    return render(request, "store/choosing_category.html", {"categories": categories})


@login_required
def choosing_sub_category(request, category_slug):

    main_category = get_object_or_404(Category, parent__isnull=True, slug=category_slug)

    subcategories = Category.objects.filter(parent=main_category)
    if request.method == "POST":
        sub_category = request.POST["subcategory_slug"]
        if not sub_category:
            messages.info(request, "please select a sub-category to adding product.")

        return redirect(
            "add_products",
            slug=request.user.slug,
            id=request.user.id,
            sub_category=sub_category,
        )
    return render(
        request,
        "store/choosing_sub_category.html",
        {"subcategories": subcategories, "main_category": main_category},
    )


def add_products(request, slug, id, sub_category):
    merchant = get_user(request, slug, id)
    sub_category_obj = get_object_or_404(Category, slug=sub_category)
    if request.method == "POST":
        form = DaynamicProductForm(category_id=sub_category_obj.id, data=request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.merchant = merchant
            product.category = sub_category_obj
            product.save()

            for field_name, value in form.cleaned_data.items():
                if field_name.startswith("attr_") and value:
                    attribute = form.fields[field_name].attribute

                    ProductAttributeValue.objects.create(
                        product=product, attribute=attribute, value=str(value)
                    )

            messages.success(request, "Product details saved! Now add images.")

            return redirect("add_product_images", slug=product.slug, id=product.id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = DaynamicProductForm(category_id=sub_category_obj.id)
    context = {"form": form, "sub_category_obj": sub_category_obj}
    return render(request, "store/add_products.html", context)


def add_product_images(request, slug, id):
    product = get_object_or_404(Product, slug=slug, id=id)
    has_primary = product.images.filter(is_primary=True).exists()
    if request.method == "POST":
        form = ProductImageForm(request.POST, request.FILES)

        if form.is_valid():

            image = form.save(commit=False)
            image.product = product
            image.save()
            return redirect("add_product_images", slug=product.slug, id=product.id)

        else:
            messages.error(
                request,
                "Please Upload A Correct Image Type only Avalible (JPG,PNG,WEBP) Formats .",
            )

    else:
        form = ProductImageForm()

    return render(
        request,
        "store/uploading_product_image.html",
        {"form": form, "product": product, "has_primary": has_primary},
    )


def add_product_inventory(request, slug, id):
    product = get_object_or_404(Product, slug=slug, id=id)
    if request.method == "POST":
        form = InventoryForm(request.POST)
        if form.is_valid():
            inventory = form.save(commit=False)
            inventory.product = product
            inventory.save()
            return redirect("published_product", slug=product.slug, id=product.id)
        else:
            messages.error(request, "Please Choose A Correct Quantity.")
    else:
        form = InventoryForm()
    context = {"form": form}
    return render(request, "store/add_product_inventory.html", context)


def published_product(request, slug, id):
    product = get_object_or_404(Product, slug=slug, id=id)
    if request.method == "POST":
        is_published = request.POST["is_published"]
        if is_published:
            product.publish = True
            product.save()
            messages.success(request, "published Successfully.")
        else:
            messages.success(request, "Saved As Draft.")
        return redirect("product_details", slug=product.slug, id=product.id)

    return render(request, "store/published_product.html", {"product": product})


def update_products(request):
    user = get_user(request, slug=request.user.slug, id=request.user.id)
    products = Product.objects.filter(merchant=user)
    context = {"products": products}
    return render(request, "store/update_products.html", context)


def update_product(request, slug, id):
    user = get_user(request, slug=request.user.slug, id=request.user.id)
    product = Product.objects.get(slug=slug, id=id)
    if product.merchant != user:
        messages.info(request, "you don't have a permission to perform this action.")
        return redirect("home")

    if request.method == "POST":
        form = DaynamicProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Product Updated Successfully.")
            return redirect("product_details", slug=product.slug, id=product.id)
        else:
            messages.info(
                request,
                "Invalid Informations Please Chack The Product Detalis And Try Agine",
            )
    else:
        form = DaynamicProductForm(instance=product)
    context = {"form": form}
    return render(request, "store/update_product.html", context)


# delete products function onlay admins or staff can use this function
def delete_products(request, slug, id):
    try:
        product = Product.objects.get(slug=slug, id=id)
        if request.method == "POST":
            # delete the product
            product.delete()
            messages.success(request, "Product Deleted Successfully..")
            return redirect("/")
        context = {"product": product}
        return render(request, "store/delete_products.html", context)
    except:
        messages.info(request, "Error!")
        return redirect("/")


# add products function to can added products from the website only admins or staff can use this function
def add_categories(request):
    if request.method == "POST" and request.user.is_staff:
        category_form = AddCategoriesForm(request.POST)
        if category_form.is_valid():
            # save the category in database
            category_form.save()
            messages.success(request, "Category Add Successfully")
            return redirect("/")
        else:
            messages.info(
                request,
                "Category Is Not Add Please Chack The Category Name And Try Agine..",
            )
    category_form = AddCategoriesForm()
    context = {"form": category_form}
    return render(request, "store/add_categories.html", context)


def contact_us(request):
    user = request.user
    if request.method == "POST":
        if user.is_authenticated:
            # Use the transaction to ensure the complete success of the code, if there is any error the code will be defeated
            with transaction.atomic():
                contact_form = Contact_Us_Form(request.POST)
                if contact_form.is_valid():
                    #  don't save the meesage before connect the meesage with the user
                    contact = contact_form.save(commit=False)
                    # connect the request user with the Contact US model to tell him the message related to this user
                    contact.user = user
                    contact.save()

                    if request.user.profile.gender == "Male":
                        messages.success(
                            request,
                            f"Your Message Sended Successfully You Well Get The Answer Soon Mr {user.profile.first_name}",
                        )
                    else:
                        messages.success(
                            request,
                            f"Your Message Sended Successfully You Well Get The Answer Soon Miss {user.profile.first_name}",
                        )
                    return redirect("/")
                else:
                    messages.info(
                        request,
                        f"Your Message Not Sended Please Chack The Informations And Try Agine!",
                    )
        else:
            messages.info(
                request, "You Have To Sign Up First And Return To Send The Message!"
            )
            return redirect("signup")
    contact_form = Contact_Us_Form()
    context = {"form": contact_form}
    return render(request, "store/contact_us.html", context)


def search_products(request):
    all_product = Product.objects.all()
    if "search_name" in request.GET:
        search_term = request.GET["search_name"]

        if search_term:
            product = all_product.filter(
                Q(name__icontains=search_term) | Q(description__icontains=search_term)
            )
            if product:
                context = {"products": product}
                return render(request, "store/search_page.html", context)
            else:
                messages.info(request, f"Not Found {search_term}")
        return render(request, "store/search_error.html")


@login_required
def add_favourites_products(request):
    if request.POST.get("action") == "post":
        user = request.user
        product_id = int(request.POST.get("product_id"))
        product = get_object_or_404(Product, id=product_id)
        if product.favourites.filter(id=user.id).exists():
            product.favourites.remove(user)
            action = "removed"
        else:
            product.favourites.add(user)
            action = "added"
        product.save()
        return JsonResponse({"action": action})


# user favourite page the display user favourite products
def user_favourites_products_page(request):
    user = request.user
    fav_products = Product.objects.filter(favourites=user)
    context = {"fav_products": fav_products}
    return render(request, "store/user_favourties_products.html", context)


# to remove products from user favourite products
def remove_favourite_product(request, slug):
    if request.method == "POST":
        product = get_object_or_404(Product, slug=slug)

        user = request.user
        # check if user is already liked the product
        if product.favourites.filter(id=user.id).exists():
            # remove the product from user favourite products
            product.favourites.remove(user)
            messages.success(
                request, "Product Removed From Your Favourite Products Successfully."
            )
        else:
            messages.error(request, "Product is not in your favourites.")
        return redirect("/")


def popular_products(request, num_products=10):
    # get the products id and use the annotate function to add likes_count filed to count favourites
    products = (
        Product.objects.values("id")
        .annotate(likes_count=Count("favourites"))
        .order_by("-likes_count")[:num_products]
    )

    # extract the products ids in list
    products_ids = products.values_list("id", flat=True)
    popular_products = (
        Product.objects.filter(id__in=products_ids)
        .annotate(likes_count=Count("favourites"))
        .order_by("-likes_count")[:num_products]
    )

    context = {"products": popular_products}
    return render(request, "store/popular_products.html", context)


def most_sold_products(request, num_products=10):
    # get the product ids with quantity and order him total_quantity the most sold product will be appear first
    product_ids_with_quantity = (
        OrderItem.objects.values("products_id")
        .annotate(total_quantity=Sum("quantity"))
        .order_by("-total_quantity")[:num_products]
    )

    # extract the products ids from product_ids_with_quantity and add him flat list,flat=True  makes sure result is list not list of tuples.
    product_ids = product_ids_with_quantity.values_list("products_id", flat=True)
    """
  filters the products where the id is in list of product_ids and 
  return sums the total of product quantity using the related_name of the model (orderitem_quantity) 
  and order him again the most sold product is well be the first"""

    products = (
        Product.objects.filter(id__in=product_ids)
        .annotate(total_quantity=Sum("orderitem__quantity"))
        .order_by("-total_quantity")
    )
    return render(
        request,
        "store/most_selld_product.html",
        {
            "products": products,
        },
    )


def mark_as_shipped(request):
    if (
        request.method == "POST"
        and request.user.is_authenticated
        and request.user.is_superuser
    ):
        try:
            order_uuid = request.POST.get("order-button")
            order = Order.objects.get(order_uuid=order_uuid)
            order.shipped = True
            order.save()
            messages.success(request, "Order marked as shipped successfully.")
            return redirect("shipped_orders_dashboard")
        except order.DoseNotExist:
            messages.success(request, "Order marked as shipped successfully.")
            return redirect("shipped_orders_dashboard")
    messages.error(request, "You do not have permission to perform this action.")
    return redirect("login") if not request.user.is_authenticated else redirect("/")
