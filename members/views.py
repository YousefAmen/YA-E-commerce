# Imports
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages

from .forms import SelectRole, UserForm, MerchentForm, CustomerForm
from .models import Merchant, Customer, User
from django.contrib.auth.decorators import login_required
from .signals import user_signed_up

# from cart.cart import Cart
import json
from django.db import transaction
from django.views.generic import DeleteView
from payment.models import Order
from store.models import Category, Product, SiteStats
from django.db.models import Count, Sum, Avg
from payment.models import Order
from django.utils import timezone
import datetime


def get_user_object(request, slug, id):
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


@login_required
def select_role(request):
    if request.method == "POST":
        form = SelectRole(request.POST)
        if form.is_valid():
            role = form.cleaned_data["role"]
            signup_data = {
                "role": role,
            }
            user_signed_up.send(
                sender=request.user.__class__,
                user=request.user,
                signup_data=signup_data,
            )
            return redirect("index")
        else:
            form = SelectRole()
            return render(request, "account/select_role.html", {"form": form})


def profile(request, slug, id):
    profile = get_user_object(request, slug=slug, id=id)
    context = {"profile": profile}
    return render(request, "account/user_profile.html", context)


@login_required
def update_profile(request, slug, id):
    profile = None
    profile_form = None
    profile = get_user_object(request, slug=slug, id=id)
    if request.user != profile.user:
        messages.error(request, "you don't have permission to edit this profile.")
        return redirect("profile", slug=request.user.slug, id=request.user.id)

    if request.method == "POST":
        if profile.user.role == "merchant":
            profile_form = MerchentForm(request.POST, request.FILES, instance=profile)
        else:
            profile_form = CustomerForm(request.POST, request.FILES, instance=profile)

        user_form = UserForm(request.POST, request.FILES, instance=user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "updated successfully.")
            return redirect("profile", slug=user.slug, id=user.id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        user_form = UserForm(instance=profile)
        if profile.user.role == "merchant":
            profile_form = MerchentForm(instance=profile)
        else:
            profile_form = CustomerForm(instance=profile)

    context = {"profile_form": profile_form, "user_form": user_form}
    return render(request, "account/update_profile.html", context)


class DeleteUserProfile(DeleteView):
    model = User
    template_name = "account/delete_profile.html"
    success_url = reverse_lazy("home")

    def check_user_onwer(self):
        user_to_delete = self.get_object()
        if self.request.user == user_to_delete:
            return user_to_delete

    def get_object(self, queryset=None):
        return User.objects.get(id=self.kwargs["id"])


@login_required
def complete_merchant(request, slug, id):
    profile = get_user_object(request, slug=slug, id=id)
    if profile.user.role != "merchant":
        messages.error(
            request, "this user is not have a merchant, please create a new account."
        )
        return redirect("account_login")
    if request.method == "POST":
        form = MerchentForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "saved successfully.")
            return redirect("profile", slug=profile.user.slug, id=profile.user.id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = MerchentForm(instance=profile)
    return render(request, "account/complete_merchant.html", {"form": form})


def merchant_grows_metrics(merchant):
    now = timezone.now()
    this_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if now.month == 1:

        last_month_start = now.replace(
            year=now.year - 1,
            month=12,
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )
        last_month_end = this_month_start
    else:
        last_month_start = now.replace(
            month=now.month - 1, day=1, hour=0, minute=0, second=0, microsecond=0
        )
        last_month_end = this_month_start
    this_month_orders = Order.objects.filter(
        merchant=merchant, order_time__gte=this_month_start
    )
    this_month_revenue = (
        this_month_orders.aggregate(revenue=Sum("amount"))["revenue"] or 0
    )
    this_month_orders_count = this_month_orders.count()

    last_month_orders = Order.objects.filter(
        merchant=merchant,
        order_time__gte=last_month_start,
        order_time__lt=last_month_end,
    )
    last_month_revenue = (
        last_month_orders.aggregate(revenue=Sum("amount"))["revenue"] or 0
    )
    last_month_orders_count = last_month_orders.count()

    if last_month_revenue > 0:
        growth_revenue = round(
            (this_month_revenue - last_month_revenue) / last_month_revenue * 100, 1
        )
    else:
        growth_revenue = 100 if this_month_revenue > 0 else 0

    # getting orders gorwth
    if last_month_orders_count > 0:
        order_growth = round(
            (this_month_orders_count - last_month_orders_count)
            / last_month_orders_count
            * 100,
            1,
        )
    else:
        order_growth = 100 if this_month_orders_count > 0 else 0

    growth_rate = round((int(growth_revenue) + order_growth) / 2, 1)

    return {
        "this_month_orders": this_month_orders,
        "this_month_revenue": this_month_revenue,
        "this_month_orders_count": this_month_orders_count,
        "last_month_orders": last_month_orders,
        "last_month_revenue": last_month_revenue,
        "last_month_orders_count": last_month_orders_count,
        "growth_revenue": growth_revenue,
        "order_growth": order_growth,
        "growth_rate": growth_rate,
    }


@login_required
def merchant_details(request, slug, id):
    user = get_user_object(slug=slug, id=id)
    try:
        merchant = Merchant.objects.get(user=user)

    except Merchant.DoesNotExist:
        messages.error(
            request, "this user dose not have a merchant, please create a new account."
        )
        return redirect("home")
    orders_count = (
        Order.objects.filter(order_items__products__merchant=merchant)
        .distinct()
        .count()
    )
    product_views_count = (
        Product.objects.filter(merchant=merchant).aggregate(views_count=Count("views"))[
            "views_count"
        ]
        or 0
    )
    most_product_views = (
        Product.objects.filter(merchant=merchant)
        .annotate(most_views=Count("views"))
        .order_by("-most_views")[:4]
    )
    total_visitors = (
        Product.objects.filter(merchant=merchant).aggregate(
            visitors_count=Count("visitors")
        )["visitors_count"]
        or 0
    )

    avg_value_orders = (
        Order.objects.filter(merchant=merchant).aggregate(avg=Avg("amount"))["avg"] or 0
    )
    total_revenue = (
        Order.objects.filter(merchant=merchant).aggregate(total=Sum("amount"))["total"]
        or 0
    )

    # calling merchant_grows_metrics
    growth_metrics = merchant_grows_metrics(merchant)
    context = {
        "merchant": merchant,
        "orders_count": orders_count,
        "product_views_count": product_views_count,
        "most_product_views": most_product_views,
        "total_visitors": total_visitors,
        "avg_value_orders": avg_value_orders,
        "total_revenue": total_revenue,
        # this month data start
        "this_month_orders": growth_metrics["this_month_orders"],
        "this_month_revenue": growth_metrics["this_month_revenue"],
        "this_month_orders_count": growth_metrics["this_month_orders_count"],
        # last month data start
        "last_month_orders": growth_metrics["last_month_orders"],
        "last_month_revenue": growth_metrics["last_month_revenue"],
        "last_month_orders_count": growth_metrics["last_month_orders_count"],
        "growth_revenue": growth_metrics["growth_revenue"],
        "order_growth": growth_metrics["order_growth"],
        "growth_rate": growth_metrics["growth_rate"],
    }
    return render(request, "account/merchant_analyzes.html", context)


def admins_dashboard(request):
    site_stats = SiteStats.objects.get(id=1)
    anonymous_visitors = site_stats.anonymous_visitor_count
    authticating_visitors = site_stats.auth_visitors.count()
    active_users = User.objects.filter(is_active=True).count()

    top_merchants = (
        Merchant.objects.annotate(top_rate=Count("visitors"))
        .distinct()
        .order_by("-top_rate")[:10]
    )

    total_visitors = site_stats.total_visitores()
    for merchant in top_merchants:
        if total_visitors > 0:
            merchant.visitors_percent = round(
                (merchant.visitor_count / total_visitors) * 100, 2
            )
        else:
            merchant.visitors_percent = 0
    total_revenue = (
        Order.objects.filter(status="shipped").aggregate(total=Sum("amount"))["total"]
        or 0
    )
    top_products = (
        Product.objects.annotate(top=Count("product"), visitors_count=Count("visitors"))
        .filter(top__gt=0)
        .order_by("-top", "-visitors_count")[:4]
    )

    context = {
        "auth_visitors": authticating_visitors,
        "anonymous_visitors": anonymous_visitors,
        "total_visitors": site_stats.total_visitores,
        "active_users": active_users,
        "top_merchants": top_merchants,
        "total_revenue": total_revenue,
        "top_products": top_products,
    }
    return render(request, "account/admins_dashboard.html", context)


def all_merchant_products(request):
    profile = get_user_object(request, slug=request.user.slug, id=request.user.id)
    if profile.user.role != "merchant":
        messages.info(request, "you don't have a permission to perform this action.")
        return redirect("home")
    products = (
        Product.objects.filter(merchant=profile)
        .annotate(view_count=Sum("views_number"))
        .filter(view_count__gt=0)
        .order_by("-view_count")
    )
    print(products)
    context = {"products": products, "merchant": profile}
    return render(request, "store/all_merchant_products.html", context)
