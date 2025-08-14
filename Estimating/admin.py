from django.contrib import admin
from .models import (
    Customer,
    TenderList,
    TenderListCustomers,
    CompletedTenderList,
    CompletedTenderCustomers,
    NotQuotingList,
    NotQuotingCustomers,
    EstimatorAcronym,
)

admin.site.register(Customer)
admin.site.register(TenderList)
admin.site.register(TenderListCustomers)
admin.site.register(CompletedTenderList)
admin.site.register(CompletedTenderCustomers)
admin.site.register(NotQuotingList)
admin.site.register(NotQuotingCustomers)

@admin.register(EstimatorAcronym)
class EstimatorAcronymAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'short_code')
    search_fields = ('full_name', 'short_code')
