from django.contrib import admin

from .models import Company, Employee, Enrollment, Mark

# Register your models here.

admin.site.register(Company)
admin.site.register(Employee)
admin.site.register(Enrollment)
admin.site.register(Mark)