import os
import io
import base64
import uuid
import secrets
import string

from http import HTTPStatus

from pycpfcnpj import cpfcnpj

from drf_yasg.utils import swagger_auto_schema
from drf_yasg.openapi import Parameter

from django.conf import settings
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import validate_email

from rest_framework.parsers import FileUploadParser
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from life_insurance_bank.serializers import BankSerializer, CompanySerializer, UploadFileSerializer
from life_insurance_bank.models import BankModel, CompanyModel
from life_insurance_bank.pagination import CompanyPagination
from life_insurance_bank.services.storage import StorageService


@csrf_exempt
def ping(request):
    data = {
        'timestamp': timezone.now(), 'build_date': os.environ.get('BUILD_DATE'), 'revision': os.environ.get('REVISION')
    }
    return JsonResponse(data)


def _generate_password():
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for index in range(20))


class BankViewSet(GenericViewSet, CreateModelMixin, ListModelMixin, UpdateModelMixin, DestroyModelMixin):

    serializer_class = BankSerializer
    queryset = BankModel.objects.all()
    http_method_names = ['get', 'post', 'put', 'delete']

    def perform_create(self, serializer):
        if BankModel.objects.filter(bank_name=serializer.validated_data.get('bank_name')).exists():
            raise ValidationError('Bank name already registered.')

        if validate_email(serializer.validated_data.get('email')):
            raise ValidationError('Invalid e-mail.')

        serializer.save(id=uuid.uuid4(), password=_generate_password())

    def _get_bank_pk(self):
        return self.request.path.split('/')[4]

    def _get_bank(self):
        try:
            bank = BankModel.objects.get(id=self._get_bank_pk())
            return bank
        except BankModel.DoesNotExist:
            raise ValidationError('Bank does not exists')

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_update(self, serializer):
        if BankModel.objects.filter(bank_name=serializer.validated_data.get('bank_name')).exists():
            raise ValidationError('Bank already registered.')

        if validate_email(serializer.validated_data.get('email')):
            raise ValidationError('Invalid e-mail.')

        serializer.save()


class CompanyViewSet(BankViewSet, GenericViewSet, CreateModelMixin, ListModelMixin, UpdateModelMixin,
                     DestroyModelMixin):

    serializer_class = CompanySerializer
    queryset = CompanyModel.objects.all()
    pagination_class = CompanyPagination
    http_method_names = ['get', 'post', 'put', 'delete']

    def perform_create(self, serializer):
        cnpj = serializer.validated_data.get('cnpj')

        if CompanyModel.objects.filter(cnpj=serializer.validated_data.get('cnpj')).exists():
            raise ValidationError('Cnpj already registered.')

        if not cpfcnpj.validate(cnpj):
            raise ValidationError('Invalid cnpf.')

        serializer.save(id=uuid.uuid4(), bank=self._get_bank(), password=_generate_password())

    def list(self, request, *args, **kwargs):
        bank_id = self.kwargs.get('bank_pk')

        try:
            filters = Q(bank=bank_id)
        except Exception as error:
            return Response(data=error.args, status=HTTPStatus.BAD_REQUEST)

        result_page = self.paginator.paginate_queryset(self.queryset.filter(filters), request)
        serializer = CompanySerializer(result_page, many=True)
        return self.paginator.get_paginated_response(serializer.data)

    def perform_update(self, serializer):
        cnpj = serializer.validated_data.get('cnpj')

        if CompanyModel.objects.filter(cnpj=serializer.validated_data.get('cnpj')).exists():
            raise ValidationError('Cnpj already registered.')

        if not cpfcnpj.validate(cnpj):
            raise ValidationError('Invalid cnpf.')

        serializer.save()


class CompanyFileUploadView(GenericViewSet, CreateModelMixin):

    serializer_class = UploadFileSerializer

    def create(self, request, bank_pk, company_pk):
        base_64_file = request.data.get('base_64_file')

        # test = base64.b64decode(bytes(base_64_file, "utf-8"))
        try:
            bank = BankModel.objects.get(id=bank_pk)
            company = CompanyModel.objects.get(id=company_pk, bank=bank)
            key_storage = f'{bank.id}-{company.id}'
            StorageService().upload(key=key_storage, buffer=base_64_file)
            return Response(data=f'File {key_storage}-file.csv has been saved.')
        except CompanyModel.DoesNotExist as error:
            raise ValidationError(error)
