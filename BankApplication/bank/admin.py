from django.contrib import admin
from  .models import AccountDetails, TransactionHistory

# Register your models here.
admin.site.register(AccountDetails)
admin.site.register(TransactionHistory)
