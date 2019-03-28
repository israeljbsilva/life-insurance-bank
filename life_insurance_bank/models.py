from django.db import models
from django.db.models.fields import CharField, UUIDField


class BankModel(models.Model):
    id = UUIDField(primary_key=True)
    bank_name = CharField(max_length=100, null=False)
    bank_code = CharField(max_length=3, null=False)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=50)

    class Meta:
        db_table = 'BANK'
        verbose_name = 'bank'
        verbose_name_plural = 'banks'


class CompanyModel(models.Model):
    id = models.UUIDField(primary_key=True)
    bank = models.ForeignKey(to=BankModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)
    official_name = models.CharField(max_length=100, null=False)
    cnpj = models.BigIntegerField(null=False)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=50)

    class Meta:
        db_table = 'COMPANY'
        verbose_name = 'company'
        verbose_name_plural = 'companies'


'''class InvitedUserModel(models.Model):
    social_security = models.CharField('social_security', primary_key=True, max_length=11, null=False)
    code = models.CharField('code', null=False, max_length=6)

    class Meta:
        db_table = 'USER'
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class InvitedFriendsModel(models.Model):
    id = models.AutoField(primary_key=True)
    invited_user = models.ForeignKey(to=InvitedUserModel, on_delete=models.CASCADE)
    social_security_friend = models.CharField('social_security_friend', max_length=11, null=False)

    class Meta:
        db_table = 'FRIENDS'
        verbose_name = 'Friends'
        verbose_name_plural = 'Friends' '''
