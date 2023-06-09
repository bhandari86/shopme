from django.urls import path
from app import views
from django.conf import settings
from django .contrib.auth import views as auth_views
from django.conf.urls.static import static
from .forms import LoginForm,MyPasswordChangeForm

urlpatterns = [
    #path('', views.home),
    path('',views.ProductView.as_view(),name="home"),
    path('product-detail/<int:pk>', views.ProductDetailsView.as_view(), name='product-detail'),
    
    
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/',views.show_cart, name="showcart"),    
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),

    path('product/',views.product,name='product'),

    path('buy/', views.buy_now, name='buy-now'),
    
    
    path('profile/', views.ProfileView.as_view(), name='profile'),
    
    
    path('topsale/', views.Topsale, name='topsale'),  
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('shoe/',views.shoe, name='shoe'),
    path('shoe/<slug:data>', views.shoe, name='shoe'),
    path('men/',views.men,name='men'),
    path('men/<slug:data>',views.men, name='menclothes' ),   
    path('women/',views.women,name='women'),
    path('women/<slug:data>',views.women, name='womenclothes' ),  
    
    path('womenshoe/',views.womenshoe,name='womenshoe'),
    path('womenshoe/<slug:data>',views.womenshoe, name='womenshoe' ),
    
    path('menshoe/',views.menshoe,name='menshoe'),
    path('menshoe/<slug:data>',views.menshoe, name='menshoe' ),
         
    path('checkout/', views.checkout, name='checkout'),
    
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm),name='login'),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'),name='passwordchange'),
    
    path('passwordchangedone/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchangedone.html'),name='passwordchangedone'),
    
    path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),
    path('registration/',views.CustomerRegistrationView.as_view(),name="customerregistration"),
    path('api/verify_payment',views.verify_payment,name='verify_payment'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:wishlist_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
