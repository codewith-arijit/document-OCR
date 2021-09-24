from django.contrib import admin
from .models import PanCard, AdharCard, VoterCard, DriverCard, Bank
# Register your models here.

admin.site.register(PanCard)
admin.site.register(AdharCard)
admin.site.register(DriverCard)
admin.site.register(VoterCard)
admin.site.register(Bank)