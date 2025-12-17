from django.urls import path

from . import views

urlpatterns = [
    path("profile/<slug:slug>/<uuid:id>/", views.profile, name="profile"),
    path(
        "profile/update/<slug:slug>/<uuid:id>/",
        views.update_profile,
        name="update_profile",
    ),
    path(
        "<uuid:id>/profile//delete/",
        views.DeleteUserProfile.as_view(),
        name="delete_profile",
    ),
    path(
        "complete_merchant/<slug:slug>/<uuid:id>/",
        views.complete_merchant,
        name="complete_merchant",
    ),
    path(
        "merchant/details/<slug:slug>/<uuid:id>/",
        views.merchant_details,
        name="merchant_details",
    ),
    path(
        "dashboard/",
        views.admins_dashboard,
        name="admins_dashboard",
    ),
]
