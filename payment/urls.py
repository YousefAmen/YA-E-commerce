from django.urls import path, include
from . import views

urlpatterns = [
    #   path('user_shipping_addresses/',user_shipping_addresses,name = 'user_shipping_addresses'),
    #   path('orders/',user_orders,name = 'user_orders'),
    #   path('user_order_detail/?=<str:order_uuid>',user_orders_detail,name = 'user_order_detail'),
    #   path('cancel_order/?=<str:order_uuid>',cancel_order,name = 'cancel_order'),
    #   path('chackout/',chackout,name = 'chackout'),
    #   path('chackout/shipping_address/',chackout_shipping_address,name = 'chackout_shipping_address'),
    #   path('add_shipping_address/',add_shippingAddress,name = 'add_shipping_address'),
    #   path('update_shipping_address/<str:token>/',update_shipping_address,name = 'update_shipping_address'),
    #   path('delete_shipping_address/<str:token>/',delete_shipping_address,name = 'delete_shipping_address'),
    #   path('order_process=?<str:token>/',order_process, name = 'order_process'),
    #   path('billing_info/',billing_info, name = 'billing_info'),
    #   path('payment_process/',payment_process, name = 'payment_process'),
    #   # shipped and unshipped page for the admin
    path(
        "management_orders_dashboard/<slug:slug>/<uuid:id>/",
        views.management_orders_dashboard,
        name="management_orders_dashboard",
    ),
    path("confirm/order/", views.confirm_order, name="confirm_order"),
    path(
        "confirm/shipped/order/", views.mark_shipped_orders, name="mark_shipped_orders"
    ),
    path(
        "confirm/delivered/order/",
        views.mark_delivered_orders,
        name="mark_delivered_orders",
    ),
    path(
        "customer/dashboard/<slug:slug>/<uuid:id>/",
        views.customer_dashboard,
        name="customer_dashboard",
    ),
    # path(
    #     "unshipped_orders_dashboard/",
    #     unshipped_orders_dashboard,
    #     name="unshipped_orders_dashboard",
    # ),
    #   path('payment_success/',payment_success,name = 'payment_success'),
    #   path('payment_failed/',payment_failed,name = 'payment_failed'),
    #   # paypal url
    #   path('paypal/', include("paypal.standard.ipn.urls")),
]
