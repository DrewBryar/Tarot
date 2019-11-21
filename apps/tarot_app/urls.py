from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^tarot$', views.tarot),
    url(r'^tarot/questionaire$', views.tarot_question),
    url(r'^user/register$', views.register),
    url(r'^user/login$', views.login),
    url(r'^user/logout$', views.logout)
]