from django.contrib import admin
from .models import FreezeHistory, Search


# Register your models here.
admin.site.register(Search)
admin.site.register(FreezeHistory)