from django.conf.urls import url, include

urlpatterns = [
    url(r'^', include('apps.tarot_app.urls')),
]