from django.contrib import admin
from drug import models

# Register your models here.

admin.site.register(models.Drugs)
admin.site.register(models.OrderDrugs)
admin.site.register(models.Order)
admin.site.register(models.Category)
admin.site.register(models.ExpiredDrugs)