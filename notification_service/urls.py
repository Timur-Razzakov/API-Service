from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from mailings.endpoint import auth_views

urlpatterns = [

    # для вывода документации о API (swagger)
    path('API_schema', get_schema_view(title="API information's",
                                       description='Это документация к тестовому API '
                                       ), name='API_schema'),
    path('docs/', TemplateView.as_view(
        template_name='index.html',
        extra_context={'schema_url': 'API_schema'}
    ), name='docs'),
    path('', auth_views.google_login),
    path('admin/', admin.site.urls),
    path('v1/', include('mailings.urls')),
    path('api-auth/', include('rest_framework.urls')),

]
