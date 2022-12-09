from django.urls import path, include
from rest_framework.routers import DefaultRouter

from mailings.endpoint.views import ClientViewSet, MessageViewSet, MailingViewSet
from .endpoint import auth_views

router = DefaultRouter()
router.register(r'mailings', MailingViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'clients', ClientViewSet)

urlpatterns = [
    path('google/', auth_views.google_auth),
    path('', include(router.urls)),
]
