from django.shortcuts import render, redirect, get_object_or_404
from .forms import ShippingAddressForms, AddShippingAddress, PaymentForm
from django.contrib import messages

# from cart.cart import Cart
from .models import Order, OrderItem
from .models import ShippingAddress
from django.db.models import Sum, Count, Avg
from members.views import get_user_object
from members.models import Merchant, Customer
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect

# from django.contrib.auth.decorators import login_required
# from store.models import Product
# from members.models import Profile
# from decimal import Decimal
# from django.db import transaction
# # import paypal stuff
# from django.urls import reverse
# from paypal.standard.forms import PayPalPaymentsForm
# from django.conf import settings
# import uuid


# def chackout(request):
#   # get the cart
#   cart = Cart(request)
#   products = cart.get_products()
#   quantity = cart.get_quantitys()
#   total = cart.total_price()
#   context = {'cart_products':products,'quantity':quantity,'total_price':total}
#   return render(request,'payment/chackout.html',context)


# def chackout_shipping_address(request):
#   if request.user.is_authenticated:
#     user_shipping_address = ShippingAddress.objects.filter(user= request.user.id)
#     if user_shipping_address.exists():
#       context = {'shipping_addresses':user_shipping_address,'orders':Order.objects.all()}
#       return render(request,'payment/choose_shipping_address.html',context)
#     else:
#       messages.warning(request,'You Dont Have Any Address,Please Add One.')
#     return render(request,'payment/choose_shipping_address.html',)
#   else:
#     messages.warning(request,'Should Be Login First To Continue Order Proccess.')
#     return redirect('login')


# def user_shipping_addresses(request):
#   shipping_addresses = ShippingAddress.objects.filter(user =request.user)
#   if shipping_addresses.exists():
#     context = {'shipping_addresses':shipping_addresses,}
#     return render(request,'members_pages/user_shipping_addresses.html',context)
#   else:
#     messages.warning(request,'You Dont Have Any Address,Please Add One.')
#     return render(request,'payment/user_shipping_addresses.html',)


# def add_shippingAddress(request):
#   if request.user.is_authenticated:
#     if request.method == 'POST':
#       form = AddShippingAddress(request.POST)
#       if form.is_valid():
#         shipping_address = form.save(commit=False)
#         shipping_address.user = request.user
#         shipping_address.shipping_email = request.user.email
#         shipping_address.save()
#         messages.success(request,'The Shipping Address Is Added Successfully..')
#         return redirect('user_shipping_addresses')
#       else:
#         for error in list(form.errors.values()):
#           messages.error(request,error)
#     form = AddShippingAddress()
#     return render(request,'store/add_shipping_address.html',{'form':form})
#   else:
#     messages.warning(request,'You Have To Login First To Can Add Address.')
#     return redirect('login')


# def update_shipping_address(request,token):
#   try:
#       address = ShippingAddress.objects.get(token=token)
#       if request.method == 'POST':
#         form = ShippingAddressForms(request.POST , instance = address)
#         if form.is_valid():
#           form.save()
#           messages.success(request,'Address Updated Successfully.')
#           return redirect('chackout_shipping_address')
#         else:
#           for error in list(form.errors.values()):
#             messages.error(request,error)
#       form = ShippingAddressForms(instance = address)
#       context = {'form':form}
#       return render(request,'store/update_address.html',context)
#   except Exception as error:
#     return render(request,'store/unavalable_page.html')


# def delete_shipping_address(request,token):
#   try:
#     address = ShippingAddress.objects.get(token=token)
#     if request.method == "POST":
#       address.delete()
#       messages.success(request,'Address Delete Successfully.')
#       return redirect('chackout_shipping_address')
#     return render(request,'store/delete_shipping_address.html',{'address':address})

#   except ShippingAddress.DoesNotExist:
#     messages.error(request, 'Address Not Found.')
#     return redirect('chackout_shipping_address')


# def order_process(request, token):
#     if request.user.is_authenticated:
#         cart = Cart(request)
#         total = float(cart.total_price())
#         products = cart.get_products()
#         quantity = cart.get_quantitys()

#         try:
#             shipping_address = ShippingAddress.objects.get(token=token)
#             shipping_address_summary = (
#                 f"{shipping_address.shipping_full_name}\n"
#                 f"{shipping_address.shipping_email}\n"
#                 f"{shipping_address.shipping_address1}\n"
#                 f"{shipping_address.shipping_address2}\n"
#                 f"{shipping_address.shipping_phone}\n"
#                 f"{shipping_address.building_name}\n"
#                 f"{shipping_address.shipping_state}\n"
#                 f"{shipping_address.shipping_city}\n"
#                 f"{shipping_address.shipping_zipcode}\n"
#                 f"{shipping_address.shipping_country}"
#             )

#             order = Order(
#                 shipping_address=shipping_address,
#                 user=request.user,
#                 amount=total,
#                 email=shipping_address.shipping_email,
#                 full_name=shipping_address.shipping_full_name,
#                 summary_shipping_address=shipping_address_summary
#             )
#             # Store order details in session as a dictionary (not as an object)
#             request.session['order_data'] = {
#                 'shipping_address_id': shipping_address.id,
#                 'user_id': request.user.id,
#                 'amount': total,
#                 'email': shipping_address.shipping_email,
#                 'full_name': shipping_address.shipping_full_name,
#                 'summary_shipping_address': shipping_address_summary
#             }


#             context = {'order':order,'cart_products': products, 'quantity': quantity}
#             return render(request, 'payment/order_details.html', context)

#         except ShippingAddress.DoesNotExist:
#             messages.error(request, 'Invalid Shipping Address.')
#             return redirect('checkout')
#     else:
#         messages.warning(request, 'You must be logged in to proceed with payment.')
#         return redirect('login')


# def billing_info(request):
#     if request.user.is_authenticated:

#         cart = Cart(request)
#         total = cart.total_price()
#         products = cart.get_products()
#         quantity = cart.get_quantitys()

#         if request.method == "POST":
#             # try:
#                 # Retrieve the order data from session
#                 with transaction.atomic():
#                   order_data = request.session.get('order_data')
#                   if not order_data:
#                       messages.error(request, 'Order not found. Please start the order process again.')
#                       return redirect('checkout')
#                   # Create and save the order instance
#                   order = Order.objects.create(
#                       shipping_address_id=order_data['shipping_address_id'],
#                       user_id=order_data['user_id'],
#                       amount=order_data['amount'],
#                       email=order_data['email'],
#                       full_name=order_data['full_name'],
#                       summary_shipping_address=order_data['summary_shipping_address']
#                   )

#                   # Create OrderItems for each product in the cart
#                   for product in products:
#                       product_quantity = quantity.get(str(product.id), 0)
#                       if product_quantity > 0:
#                         if product.instock != 0:
#                             OrderItem.objects.get_or_create(
#                                 order=order,
#                                 products=product,
#                                 user=request.user,
#                                 price=product.price,
#                                 quantity=product_quantity
#                             )

#                             product.instock -= product_quantity
#                             product.save()
#                         else:
#                           messages.info(request, f'"{product.name}" is now out of stock.')

#                   # Clear the session and cart
#                   for key in list(request.session.keys()):
#                     if key == "session_key":
#                       del request.session[key]
#                   Profile.objects.filter(user=request.user).update(cart="")

#                 messages.success(request,f'Order Pleced Successfully {request.user.profile.first_name}.')
#                 return redirect('/')

#             # except Exception as error:
#             #     messages.info(request, f'Order not placed. Please try again')
#             #     return redirect('/')
#         host = request.get_host()
#         paypal_dict = {
#           "business": settings.PAYPAL_RECEIVER_EMAIL,
#           "amount": total,
#           "item_name":"order_items",
#           "no_shipping":'2',
#           "invoice": str(uuid.uuid4()),
#           "currency_code" : "USD",
#           "notify_url": f"https://{host}{reverse('paypal-ipn')}",
#           "return_url": f"https://{host}{reverse('payment_success')}",
#           "cancel_url": f"https://{host}{reverse('payment_failed')}",
#         }
#         # create the paypal forms
#         paypal_form = PayPalPaymentsForm(initial=paypal_dict)
#         billing_forms = PaymentForm()
#         context = {'payment_form': billing_forms,'paypal_form':paypal_form}
#         return render(request, 'payment/billing_info.html', context)
#     else:
#         messages.warning(request, 'You must be logged in to proceed with payment.')
#         return redirect('login')


# def user_orders(request):
#   filter_user_orders=Order.objects.filter(user=request.user)
#   context = {'user_orders':filter_user_orders,}
#   return render(request,'payment/user_orders.html',context)


# def user_orders_detail(request,order_uuid):
#   order=Order.objects.get(order_uuid=order_uuid)
#   orderitem = OrderItem.objects.filter(order=order.id)
#   context = {'order':order,'orderitem':orderitem}
#   return render(request,'payment/user_orders_detail.html',context)


# def cancel_order(request,order_uuid):
#   try:
#     order = Order.objects.get(order_uuid = order_uuid)
#     orderitem = OrderItem.objects.filter(order=order.id)
#     if not order.shipped:
#       if request.method == 'POST':
#         order.delete()
#         messages.success(request,'Order Cancel Successfully.')
#         return redirect('user_orders')
#       context = {'order':order,'orderitem':orderitem}
#       return render(request,'payment/cancel_order.html',context)
#     else:
#       messages.info(request,"Order Can't Cancel This Order Is Shipped.")
#       return redirect('user_orders')
#   except Exception as error:
#     messages.error(request,f'{error}')


# def payment_process(request):
#   if request.user.is_authenticated:
#     billing_forms = PaymentForm(request.POST or None)
#     return render(request, 'payment/payment_page.html')
#   else:
#     messages.warning(request,'Access Is Denied')
#     return redirect('/')


@login_required
def management_orders_dashboard(request, slug, id):

    user = get_user_object(slug, id)
    merchant = None
    if user.role == "merchant":
        merchant = Merchant.objects.get(user=user)
    else:
        messages.info(request, "you don't have permission to access this page.")
        return redirect("home")
    order_status = {}
    for status in ["pending", "shipped", "confirmed", "delivered"]:
        order_status[f"{status}_status"] = Order.objects.filter(
            status=status, merchant=merchant
        ).prefetch_related("order_items")
    all_orders = Order.objects.filter(merchant=merchant)
    total_customers = (
        all_orders.aggregate(customers=Count("customer"))["customers"] or 0
    )

    total_orders = all_orders.count()
    orders_revenue = all_orders.aggregate(total=Sum("amount"))["total"] or 0
    avg_orders_value = all_orders.aggregate(avg=Avg("amount"))["avg"] or 0
    context = {
        "orders_revenue": orders_revenue,
        "avg_orders_value": avg_orders_value,
        "total_orders": total_orders,
        "order_status": order_status,
        "total_customers": total_customers,
    }
    return render(request, "payment/management_orders_dashboard.html", context)


@require_POST
@csrf_protect
def confirm_order(request):
    order_id = request.POST["order_id"]
    if not order_id:
        return JsonResponse({"message": "failed", "error": "No Order Id Is Provided."})

    merchant = get_object_or_404(Merchant, user=request.user)
    order = get_object_or_404(Order, id=order_id, merchant=merchant)
    order.status = "confirmed"
    order.save()

    return JsonResponse({"message": "success", "order_id": str(order.id)})


@require_POST
@csrf_protect
def mark_shipped_orders(request):
    order_id = request.POST["order_id"]
    if not order_id:
        return JsonResponse({"message": "failed", "error": "No Order Id Is Provided."})

    merchant = get_object_or_404(Merchant, user=request.user)
    order = get_object_or_404(Order, id=order_id, merchant=merchant)
    order.status = "shipped"
    order.save()
    return JsonResponse({"message": "success", "order": str(order.full_name)})


@require_POST
@csrf_protect
def mark_delivered_orders(request):
    order_id = request.POST["order_id"]
    if not order_id:
        return JsonResponse({"message": "failed", "error": "No Order Id Is Provided."})

    merchant = get_object_or_404(Merchant, user=request.user)
    order = get_object_or_404(Order, id=order_id, merchant=merchant)
    order.status = "delivered"
    order.save()
    return JsonResponse({"message": "success", "order": str(order.full_name)})


def customer_dashboard(request, slug, id):
    user = get_user_object(slug, id)
    if user.role != "customer":
        return messages.error(
            request, "you don't have a permission to access this page."
        )

    customer = Customer.objects.get(user=user)
    order_status = {}
    for status in ["shipped", "pending", "delivered"]:
        order_status[f"{status}_orders"] = Order.objects.filter(
            customer=customer, status=status
        )
    customer_orders = Order.objects.filter(customer=customer).order_by("order_time")
    total_orders = customer_orders.count()

    return render(
        request,
        "account/customer_dashboard.html",
        {
            "cusomter_orders": customer_orders,
            "order_status": order_status,
            "total_orders": total_orders,
        },
    )


# # def view_that_asks_for_money(request):

# #     # What you want the button to do.
# #     paypal_dict = {
# #         "business": "receiver_email@example.com",
# #         "amount": "10000000.00",
# #         "item_name": "name of the item",
# #         "invoice": "unique-invoice-id",
# #         "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
# #         "return": request.build_absolute_uri(reverse('your-return-view')),
# #         "cancel_return": request.build_absolute_uri(reverse('your-cancel-view')),
# #         "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
# #     }

# #     # Create the instance.
# #     form = PayPalPaymentsForm(initial=paypal_dict)
# #     context = {"form": form}
# #     return render(request, "payment/payment_page.html", context)


# def payment_success(request):
#   return render(request,'payment/payment_success.html')


# def payment_failed(request):
#   return render(request,'payment/payment_failed.html')
