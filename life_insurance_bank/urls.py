from django.urls import path, include
from rest_framework_nested import routers
from life_insurance_bank.views import BankViewSet, CompanyViewSet, CompanyFileUploadView


app_name = 'life_insurance_bank'


bank_router = routers.DefaultRouter(trailing_slash=False)
bank_router.register(r'bank', BankViewSet, base_name='bank')

companies_router = routers.NestedSimpleRouter(bank_router, r'bank', lookup='bank', trailing_slash=False)
companies_router.register(r'company', CompanyViewSet, 'company')

upload_router = routers.NestedSimpleRouter(companies_router, r'company', lookup='company', trailing_slash=False)
upload_router.register(r'upload', CompanyFileUploadView, 'upload')


urlpatterns = (
    path('', include(bank_router.urls)),
    path('', include(upload_router.urls)),
    path('', include(companies_router.urls)),

)
