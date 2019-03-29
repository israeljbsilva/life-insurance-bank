from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from life_insurance_bank import urls
from life_insurance_bank.views import ping


api_path = 'api/v1/'


schema_view = get_schema_view(
    openapi.Info("Life Insurance Bank", 'v1'), public=True
)


urlpatterns = [
    path('api-docs/', schema_view.with_ui(), name='schema-swagger-ui'),
    path(api_path, include(urls, urls.app_name)),
    path('ping/', ping, name='ping')
]
