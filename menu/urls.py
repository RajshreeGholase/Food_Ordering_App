from django.urls import path
from . import views

urlpatterns = [
    path('', views.MenuList.as_view(), name='home'),
    path('item/<int:pk>/', views.MenuItemDetail.as_view(), name='menu_item'),

    #Cart URLs (NEW)
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),

    #Order URL (NEW)
    path('place-order/', views.place_order, name='place_order'),

]
