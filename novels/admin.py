from django.contrib import admin
from .models import Novels
# Register your models here.


class NovelsAdmin(admin.ModelAdmin):
    list_display = ['title', 'code', 'category', 'review']


admin.site.register(Novels, NovelsAdmin)