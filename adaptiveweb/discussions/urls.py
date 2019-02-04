from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^signup', views.signup, name='signup'),
    url(r'^getQueryRecommendation', views.getQueryRecommendation,
        name='getQueryRecommendation'),
    url('', views.viewPosts, name='viewPosts'),
]
