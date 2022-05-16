from django.urls import path
from django.views.generic import TemplateView
from core.views import *

from django.views.generic import TemplateView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),

    path('create_post/', create_post, name='create_post'),
    path('post/<int:id>', show_post, name='show_post'),
    path('delete_post_page/', delete_post_page, name='delete_post_page'),
    path('delete_post/<int:id>', delete_post, name='delete_post'),
    path('<str:category>', home, name='home'),
    path('query/<str:category>', query, name='query'),
    path('', home, name='home'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),

    # product order
    path('order_list/<int:id>', order_list, name='order_list'),
    path('order_list/', order_list, name='my_order_list'),
    path('place_order/', place_order, name='place_order'),
    path('success/', success, name='success'),

    # admin
    path('admin/handle', handle_orders, name='handle_orders'),
    
]