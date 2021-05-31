from django.contrib import admin
from .models import Candidate, MonthSalary, Recruitment, Staff, StaffSalaryBase, WorkDay

# Register your models here.
admin.site.register(Staff)
admin.site.register(Recruitment)
admin.site.register(Candidate)
admin.site.register(StaffSalaryBase)
admin.site.register(WorkDay)
admin.site.register(MonthSalary)