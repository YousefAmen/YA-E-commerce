from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("About Us/", views.about, name="about"),
    path(
        "product/details/<slug:slug>/<uuid:id>/",
        views.product_details,
        name="product_details",
    ),
    path("product/<str:cat>/", views.category, name="category"),
    path("categories/", views.all_categories, name="all_categories"),
    path(
        "add_products/<slug:slug>/<uuid:id>/<str:sub_category>/",
        views.add_products,
        name="add_products",
    ),
    path(
        "adding/images/<slug:slug>/<uuid:id>/",
        views.add_product_images,
        name="add_product_images",
    ),
    path(
        "adding/inventory/<slug:slug>/<uuid:id>/",
        views.add_product_inventory,
        name="add_product_inventory",
    ),
    path(
        "adding/published/product/<slug:slug>/<uuid:id>/",
        views.published_product,
        name="published_product",
    ),
    path(
        "update_products/",
        views.update_products,
        name="update_products",
    ),
    path(
        "update_products/update/<slug:slug>/<uuid:id>/product/",
        views.update_product,
        name="update_product",
    ),
    path(
        "update_products/delete/<slug:slug>/<uuid:id>/product/",
        views.delete_products,
        name="delete_products",
    ),
    path("add_categories/", views.add_categories, name="add_categories"),
    path("contact_us/", views.contact_us, name="contact_us"),
    path("search/", views.search_products, name="search_products"),
    path("offers/", views.discount_products, name="offers_product"),
    path(
        "most_selled_products/", views.most_sold_products, name="most_selled_products"
    ),
    path(
        "user_favourites_products_page/",
        views.user_favourites_products_page,
        name="user_favourites_products_page",
    ),
    path(
        "add_favourites_products/",
        views.add_favourites_products,
        name="add_favourites_products",
    ),
    path(
        "remove_favourite_product/remove/<str:slug>",
        views.remove_favourite_product,
        name="remove_favourite_product",
    ),
    path("popular_products/", views.popular_products, name="popular_products"),
    path("mark_as_shipped/", views.mark_as_shipped, name="mark_as_shipped"),
    path(
        "choosing/main/category/",
        views.choosing_product_category,
        name="choosing_product_category",
    ),
    path(
        "choosing/sub/category/<slug:category_slug>/",
        views.choosing_sub_category,
        name="choosing_sub_category",
    ),
]
