from django.db import models
from django.contrib.auth.models import User
# Create your models here.

ROLE_CHOICES = (
  (1, "Quản Lý"),
  (2, "Nhân Viên")
)

DEPARTMENT_CHOICES = (
  ('N', 'Nhân Sự'),
  ('H', 'Hành Chính'),
  ('D', 'Đào Tạo')
)

QUALIFICATION_CHOICES = {
  ("CD", "Cao Đẳng"),
  ("DH", "Đại Học"),
  ("TH", "Thạc Sĩ"),
  ("TS", "Tiến Sĩ")
}

SALARY_DICT = {
  "ADMINISTRATIVE": 1,
  "OVERTIME": 1.5,
  "DAYOFF": 2,
  "HOLIDAY": 2.5,
}
class Staff(models.Model):
  staff_id = models.CharField(max_length=5, unique=True)
  staff_name = models.CharField(max_length=50)
  role = models.IntegerField(choices=ROLE_CHOICES, default=2)
  phone = models.CharField(max_length=20)
  card_id = models.CharField(max_length=20, unique=True)
  address = models.CharField(max_length=200)
  department = models.CharField(choices=DEPARTMENT_CHOICES, max_length=1)
  qualification = models.CharField(choices=QUALIFICATION_CHOICES,max_length=2, null=True, blank=True)
  def __str__(self):
    return self.staff_name

class Recruitment(models.Model):
  rec_name = models.CharField(max_length=50)
  positions = models.CharField(max_length=200)
  describe = models.CharField(max_length=500)
  quantity = models.IntegerField()
  requirements = models.CharField(max_length=500)
  def __str__(self):
    return self.rec_name

class Candidate(models.Model):
  c_name = models.CharField(max_length=50)
  dob = models.DateField()
  phone = models.CharField(max_length=20)
  card_id = models.CharField(max_length=20, unique=True)
  address = models.CharField(max_length=200)
  qualification = models.CharField(max_length=200)
  recruitment = models.ForeignKey(Recruitment, related_name='candidates', on_delete=models.CASCADE)
  def __str__(self):
    return self.c_name

class StaffSalaryBase(models.Model):
  staff = models.OneToOneField(Staff, related_name='salaryBase', on_delete=models.CASCADE)
  basic_salary = models.IntegerField()
  salary_coefficient = models.FloatField()
  allowances_coefficient = models.FloatField()
  def __str__(self):
    return self.staff.staff_name

class WorkDay(models.Model):
  staff = models.ForeignKey(Staff, related_name='workDay', on_delete=models.CASCADE)
  day = models.IntegerField()
  month = models.IntegerField(null=True)
  year = models.IntegerField(null=True)
  start_time = models.TimeField(null=True)
  end_time = models.TimeField(null=True)
  def __str__(self):
    return self.staff.staff_name + f" {self.day}/{self.month}/{self.year}"

class MonthSalary(models.Model):
  month = models.IntegerField(null=True)
  year = models.IntegerField(null=True)
  administrative = models.FloatField()
  overtime = models.FloatField()
  dayoff = models.FloatField()
  holiday = models.FloatField()
  staff = models.ForeignKey(Staff, related_name='monthSalarys', on_delete=models.CASCADE)
  @property
  def get_month_salary(self):
    basic_salary = self.staff.salaryBase.basic_salary
    allowances_coefficient = self.staff.salaryBase.allowances_coefficient
    salary_coefficient = self.staff.salaryBase.salary_coefficient
    salary = (self.administrative * SALARY_DICT["ADMINISTRATIVE"] + self.overtime * SALARY_DICT["OVERTIME"] + self.dayoff * SALARY_DICT["DAYOFF"] + self.holiday * SALARY_DICT["HOLIDAY"]) * basic_salary
    return salary
  @property
  def get_month_allowance(self):
    basic_salary = self.staff.salaryBase.basic_salary
    allowances_coefficient = self.staff.salaryBase.allowances_coefficient
    salary_coefficient = self.staff.salaryBase.salary_coefficient
    allowances = basic_salary * (allowances_coefficient + salary_coefficient)
    return allowances
  @property
  def get_month_total_salary(self):
    return self.get_month_salary + self.get_month_allowance
  def __str__(self):
    return self.staff.staff_name