from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.create_page, name="new_page"),
    path("wiki/<str:title>",views.page,name="page_name"),
    path("edit/<str:title>", views.edit_page, name="edit_page"),
    path("random",views.random_page,name="random_page"),
    path("search",views.search,name="search")
]
