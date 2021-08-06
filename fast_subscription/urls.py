from django.urls import path
from . import views



app_name = 'fast_subscription'

urlpatterns = [
    path('', views.Home ,name='home'),

    # path('login-signup/', views.login_signup, name='login_signup'),


    path('get-order/', views.Get_order ,name='get_order'),
    path('subscription/', views.Get_subscription ,name='subscription'),
    path('all-products/', views.get_product ,name='get_product'),
    path('products/', views.product ,name='product'),

    path('update-subscription/', views.update_subscription ,name='update_subscription'),
    path('cancel-subscription/', views.cancel_subscription ,name='cancel_subscription'),
    path('renew-subscription/', views.renew_subscription ,name='renew_subscription'),
    path('create-subscription/', views.create_subscription ,name='create_subscription'),
    path('create-product/', views.create_product ,name='create_product'),
    path('get-product-by-ref/', views.get_product_by_ref ,name='get_prod_by_ref'),
    path('get-all-subscription/', views.Get_all ,name='get_all'),

]
