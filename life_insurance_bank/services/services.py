from .storage import StorageService
from django.conf import settings
from life_insurance_bank.models import CompanyModel


def update_base_64_file(bank, company, base_64_file):
    key_storage = f'{bank.id}-{company.id}'
    StorageService().upload(key=key_storage, buffer=base_64_file)
    upload_file_full_url = f'{settings.STORAGE_URL}/{settings.STORAGE_BUCKET_NAME}/' \
        f'{settings.STORAGE_PREFIX_NAME}{key_storage}-file.csv'
    CompanyModel(
        id=company.id, bank=bank, name=company.name, official_name=company.official_name,
        cnpj=company.cnpj, data_load=upload_file_full_url, email=company.email,
        password=company.password).save(force_update=True)
