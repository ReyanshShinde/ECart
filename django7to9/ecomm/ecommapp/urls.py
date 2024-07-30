from django.urls import path
from ecommapp import views
from ecommapp.views import SimpleView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    
    path('',views.home),
    path('about',views.about),
    path('contact/<a>/<b>',views.contact),
    path('myview',SimpleView.as_view()),
    path('index',views.index),
    path('catfilter/<cv>',views.catfilter),
    path('sort/<sv>',views.sort),
    path('range',views.range),
    path('login',views.user_login),
    path('logout',views.user_logout),
    path('reg',views.register),
    path('pd/<pid>',views.product_detail),
    path('addtocart/<pid>',views.addtocart),
    path('cart',views.cart),
    path('updateqty/<qv>/<cid>',views.updateqty),
    path('remove/<pid>',views.remove),
    path('po',views.place_order),
    path('makepayment',views.makepayment),
    path('sendmail',views.sendusermail),
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)