from rest_framework.serializers import ModelSerializer

from .models import BankModel, CompanyModel


class BankSerializer(ModelSerializer):

    class Meta:
        model = BankModel
        fields = '__all__'
        read_only_fields = ('id', 'password')


class CompanySerializer(ModelSerializer):

    class Meta:
        model = CompanyModel
        fields = '__all__'
        read_only_fields = ('id', 'bank', 'password')
