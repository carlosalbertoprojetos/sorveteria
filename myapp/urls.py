from django.urls import path
from myapp import views

urlpatterns = [
    path("", views.index, name="index"),
    path("menu", views.menu, name="menu"),
    path("sacola", views.adicionar_sacola, name="adicionar_sacola"),
    path(
        "atualiza_quantidade_sacola/",
        views.atualiza_quantidade_sacola,
        name="atualiza_quantidade_sacola",
    ),
    path("remove_item_sacola/", views.remove_item_sacola, name="remove_item_sacola"),
    path("checkout-pedido/", views.checkout_pedido, name="checkout_pedido"),
]
