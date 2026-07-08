from django.urls import path
from . import views


app_name = "main"

urlpatterns = [
    path("", views.product_list, name='product_list'),
    path("<slug:slug>/", views.product_detail, name='product_detail'),
    path("category/<slug:category_slug>/", views.product_list, name="product_list_by_categories"),
    path("about/", views.about, name="about"),
    path("delivery/", views.delivery, name="delivery"),
    path("returns/", views.returns, name="returns"),
    path("contacts/", views.contacts, name="contacts"),
]
