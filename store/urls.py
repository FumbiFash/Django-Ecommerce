from . import views
from django.urls import path 

urlpatterns = [
    path("",views.store,name="store"),
    path('checkout/',views.checkout,name="checkout"),
    path('cart/',views.cart,name="cart"),
    path("update_item",views.updatedItem),
    path("process_order",views.processOrder),
    path("thank_you",views.thankyou,name = "thankyou"),
    path("services",views.services,name = "services"),
    path("about",views.about,name = "about"),
    path("contact",views.contact,name = "contact"),
    path("login",views.login_user,name = "login"),
    path("register",views.createUser,name = "register"),
    path("logout",views.logoutUser,name = "logout")

]