from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView

from . import views  # import views so we can use them in urls.

app_name = 'substitut'

urlpatterns = [
    url(r'^(?P<produit_id>[0-9]+)/$', views.detail),
    url(r'^search', views.search, name='search'),
    url(r'^mentionslegales/$', views.mentionslegales, name='mentionslegales'),
    url(r'^useraccount/$', views.useraccount, name='useraccount'),
    url(r'^userproducts/$', views.userproducts, name='userproducts'),
    url(r'^products/$', views.products, name='products'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', LoginView.as_view(template_name='substitut/login.html'), name='login'),
    url(r'^logout/$', LogoutView.as_view(template_name='substitut/logout.html'), name='logout'),
]
