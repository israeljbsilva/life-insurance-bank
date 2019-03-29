import os
import io
import base64
import urllib
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

from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from life_insurance_bank.serializers import BankSerializer, CompanySerializer, UploadFileSerializer, EmployeeSerializer
from life_insurance_bank.models import BankModel, CompanyModel
from life_insurance_bank.pagination import CompanyPagination
from life_insurance_bank.services.storage import StorageService
from life_insurance_bank.services import services


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


class EmployeeViewSet(GenericViewSet, CreateModelMixin, ListModelMixin, DestroyModelMixin):

    serializer_class = EmployeeSerializer

    def get_queryset(self):
        try:
            bank = BankModel.objects.get(id=self.kwargs.get('bank_pk'))
            company = CompanyModel.objects.get(id=self.kwargs.get('company_pk'), bank=bank)
            return bank, company
        except CompanyModel.DoesNotExist as error:
            raise ValidationError(error)

    def create(self, request, *args, **kwargs):
        bank, company = self.get_queryset()
        name = request.data.get('name')
        cpf = request.data.get('cpf')

        list_insert = bytes(f'{name};{cpf}\n', encoding='utf-8')
        file_data = urllib.request.urlopen(company.data_load)
        datatowrite = file_data.read()
        datatowrite += list_insert

        base_64_file = base64.b64encode(datatowrite).decode("utf-8")
        services.update_base_64_file(bank=bank, company=company, base_64_file=base_64_file)

    def list(self, request, *args, **kwargs):
        _, company = self.get_queryset()
        list_response = []
        file_data = urllib.request.urlopen(company.data_load)
        datatowrite = file_data.readlines()
        for employee in datatowrite:
            response = {}
            file_decode = employee.decode("utf-8")
            context = file_decode.split(';')
            response['name'] = context[0]
            response['cpf'] = context[1].replace('\n', '')
            list_response.append(response)
        return Response(data=list_response)

    def destroy(self, request, *args, **kwargs):
        bank, company = self.get_queryset()
        cpf = self.kwargs.get('pk')
        file_data = urllib.request.urlopen(company.data_load)
        datatowrite = file_data.readlines()
        for index, employee in enumerate(datatowrite):
            if cpf in employee.decode("utf-8"):
                datatowrite.pop(index)
        join_bytes = bytes('', encoding='utf-8').join(datatowrite)
        base_64_file = base64.b64encode(join_bytes).decode("utf-8")
        services.update_base_64_file(bank=bank, company=company, base_64_file=base_64_file)
        return Response(data=f'{cpf} removed')


class FileUploadViewSet(EmployeeViewSet, GenericViewSet, CreateModelMixin):

    serializer_class = UploadFileSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        bank, company = self.get_queryset()
        base_64_file = request.data.get('base_64_file')
        services.update_base_64_file(bank=bank, company=company, base_64_file=base_64_file)
        return Response(data=f'File file.csv has been saved.')
