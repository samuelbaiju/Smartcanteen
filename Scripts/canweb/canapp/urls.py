from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import signup_view,home_view,inhome_view,add_menu_item,edit_menu,delete_menu,add_to_cart,remove_from_cart,bill_summary_view,view_bills
from django.shortcuts import render
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', home_view, name='home'),
    path('signup/', signup_view, name='signup'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('inhome/', inhome_view, name='inhome'),
    path('add-menu/', add_menu_item, name='add_menu'),
    path('edit/<int:item_id>/', edit_menu, name='edit_menu'),
    path('delete/<int:item_id>/', delete_menu, name='delete_menu'),
    path('inhome/add-to-cart/<int:item_id>/', add_to_cart, name='add_to_cart'),
    path('inhome/remove-from-cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('bill-summary/', bill_summary_view, name='bill_summary'),
    path('view-bills/', view_bills, name='view_bills'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)