from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


# Create your models here.
class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    bill_to = models.CharField(max_length=255, null=True, blank=True)
    fname = models.CharField(max_length=100, null=True, blank=True)
    lname = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    mob = models.CharField(max_length=50, null=True, blank=True)
    street1 = models.CharField(max_length=255, null=True, blank=True)
    street2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    on_stop = models.BooleanField(default=False)
    is_unverified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = 'customers'


class TenderList(models.Model):
    tender_id = models.AutoField(primary_key=True)
    tender_name = models.CharField(max_length=255)
    tender_received_date = models.DateField()
    tender_due_date = models.DateField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    is_not_quoting = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    quote_created = models.BooleanField(default=False)
    added_by = models.CharField(max_length=255, null=True, blank=True)
    estimator = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    email_id = models.CharField(max_length=255, unique=True)

    customers = models.ManyToManyField(Customer, through='TenderListCustomers')

    class Meta:
        managed = False
        db_table = 'tender_list'


class TenderListCustomers(models.Model):
    id = models.AutoField(primary_key=True)
    tender = models.ForeignKey(TenderList, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'tender_list_customers'


class CompletedTenderList(models.Model):
    completed_tender_id = models.AutoField(primary_key=True)
    tender_name = models.CharField(max_length=255)
    tender_received_date = models.DateField()
    tender_due_date = models.DateField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    added_by = models.CharField(max_length=255, null=True, blank=True)
    estimator = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    email_id = models.CharField(max_length=255, unique=True)

    customers = models.ManyToManyField(Customer, through='CompletedTenderCustomers')

    class Meta:
        managed = False
        db_table = 'completed_tender_list'


class CompletedTenderCustomers(models.Model):
    id = models.AutoField(primary_key=True)
    completed_tender = models.ForeignKey(CompletedTenderList, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'completed_tender_customers'


class NotQuotingList(models.Model):
    not_quoting_id = models.AutoField(primary_key=True)
    tender_name = models.CharField(max_length=255)
    tender_received_date = models.DateField()
    tender_due_date = models.DateField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    added_by = models.CharField(max_length=255, null=True, blank=True)
    estimator = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    email_id = models.CharField(max_length=255, unique=True)

    customers = models.ManyToManyField(Customer, through='NotQuotingCustomers')

    class Meta:
        managed = False
        db_table = 'not_quoting_list'


class NotQuotingCustomers(models.Model):
    id = models.AutoField(primary_key=True)
    not_quoting = models.ForeignKey(NotQuotingList, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'not_quoting_customers'

class Builder(models.Model):
    name = models.CharField(max_length=255, unique=True)
    contact_person = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=255)
    builder = models.ForeignKey(Builder, on_delete=models.CASCADE)  # Remove 'Estimating.'
    estimator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_from = models.ForeignKey('TenderList', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Package(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=[('door', 'Door Hardware'), ('sanitary', 'Sanitary')])
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Door(models.Model):
    name = models.CharField(max_length=255)
    material = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    rating = models.CharField(max_length=255)

    def __str__(self):
        return self.name



def get_added_by_short(self):
    return settings.ESTIMATOR_ACRONYMS.get(self.added_by.split('@')[0], self.added_by)

def get_estimator_short(self):
    return settings.ESTIMATOR_ACRONYMS.get(self.estimator, self.estimator)

TenderList.get_added_by_short = get_added_by_short
TenderList.get_estimator_short = get_estimator_short

class EstimatorAcronym(models.Model):
    full_name = models.CharField(max_length=100, unique=True)
    short_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.full_name} → {self.short_code}"
