from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^tarot$', views.tarot),
    url(r'^tarot/questionaire$', views.tarot_question),
    url(r'^tarot/questionaire/process$', views.question_process),
    url(r'^tarot/questionaire/(?P<category>\w+)/mood$', views.tarot_question_mood),
    url(r'^tarot/questionaire/(?P<category>\w+)/mood_ask$', views.submit_read),
    url(r'^reading/(?P<user_id>\d+)/(?P<reading_id>\d+)$', views.show_card_result),
    url(r'^user/(?P<user_id>\d+)$', views.showuser),
    url(r'^reading/(?P<reading_id>\d+)/delete$', views.delete),
    url(r'^reading/(?P<reading_id>\d+)/like$', views.like),
    url(r'^reading/(?P<reading_id>\d+)/unlike$', views.unlike),
    url(r'^user/register$', views.register),
    url(r'^user/login$', views.login),
    url(r'^user/logout$', views.logout)
]