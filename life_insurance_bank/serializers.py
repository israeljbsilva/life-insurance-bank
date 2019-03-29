from rest_framework import serializers

from .models import BankModel, CompanyModel


class BankSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankModel
        fields = '__all__'
        read_only_fields = ('id', 'password')


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyModel
        fields = '__all__'
        read_only_fields = ('id', 'bank', 'password')


class UploadFileSerializer(serializers.Serializer):
   base_64_file = serializers.CharField()
