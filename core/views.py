from django.http.response import JsonResponse
from core.models import Candidate, MonthSalary, Recruitment, Staff, StaffSalaryBase, WorkDay
from django.shortcuts import redirect, render
from core.forms import CandidateForm, DatePickerForm, RecruitmentForm, StaffForm
from django.views.generic import View
from django.urls import reverse
from django.core import serializers
from django.db.models import Q
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required
from datetime import datetime
import re
# Create your views here.
@login_required
def home(request):
  return render(request, 'home.html')

@login_required
def profile_management(request):
    staffs = Staff.objects.all()
    context = {
      'staffs': staffs,
      'form': StaffForm,
    }
    return render(request, 'profile_management.html', context)

SALARY_COEF_DICT = {
  "CD": 2.10,
  "DH": 2.34,
  "TH": 2.66,
  "TS": 3.00,
}
ALLOWANCE_COEF_DICT = {
  1: 2.00,
  2: 1.00,
}
class ProfileManagementAjaxView(View):
  http_method_names = ['GET', 'POST', 'PUT', 'DELETE']
  def dispatch(self, *args, **kwargs):
    if self.request.is_ajax() and self.request.POST:
      if self.request.POST.get('_method') == "POST":
        return self.post(*args, **kwargs)
      elif self.request.POST.get('_method') == "PUT":
        return self.put(*args, **kwargs)
      elif self.request.POST.get('_method') == "DELETE":
        return self.delete(*args, **kwargs)
    return super().dispatch(self.request, *args, **kwargs)

  def post(self, *args, **kwagrs):
    try:
      form = StaffForm(self.request.POST)
      if form.is_valid():
        staff = Staff()
        staff.staff_id = form.cleaned_data["staff_id"]
        staff.staff_name = form.cleaned_data["staff_name"]
        staff.role = int(form.cleaned_data["role"])
        staff.card_id = form.cleaned_data["card_id"]
        staff.address = form.cleaned_data["address"]
        staff.phone = form.cleaned_data["phone"]
        staff.department = form.cleaned_data["department"]
        staff.qualification = form.cleaned_data["qualification"]
        staff.save()
        staff_display = {
          'role': staff.get_role_display(),
          'department': staff.get_department_display(),
        }
        ser_instance = serializers.serialize('json', [ staff, ])
        staffSalaryBase = StaffSalaryBase()
        staffSalaryBase.staff = staff
        staffSalaryBase.basic_salary = 50000
        staffSalaryBase.salary_coefficient = SALARY_COEF_DICT[staff.qualification]
        staffSalaryBase.allowances_coefficient = ALLOWANCE_COEF_DICT[staff.role]
        staffSalaryBase.save()
        return JsonResponse({"staff": ser_instance, "staff_display": staff_display, 'method': 'POST'}, status=200)
    except IntegrityError as e:
      error_cause = ''
      if 'staff_id' in e.args[0]:
        error_cause = "Staff ID"
      elif 'card_id' in e.args[0]:
        error_cause = "Card ID"
      return JsonResponse({"result": "error","error": f"{error_cause} existed, please try another.", 'method': 'POST'}, status=200)

  def put(self, *args, **kwagrs):
    try:
      form = StaffForm(self.request.POST)
      if form.is_valid():
        staff = Staff.objects.get(pk=int(self.request.POST['index']))
        staff.staff_id = form.cleaned_data["staff_id"]
        staff.staff_name = form.cleaned_data["staff_name"]
        staff.role = int(form.cleaned_data["role"])
        staff.card_id = form.cleaned_data["card_id"]
        staff.address = form.cleaned_data["address"]
        staff.phone = form.cleaned_data["phone"]
        staff.department = form.cleaned_data["department"]
        staff.qualification = form.cleaned_data["qualification"]
        staff.save()
        staff_display = {
          'role': staff.get_role_display(),
          'department': staff.get_department_display(),
        }
        ser_instance = serializers.serialize('json', [ staff, ])
        staffSalaryBase = staff.salaryBase
        staffSalaryBase.salary_coefficient = SALARY_COEF_DICT[staff.qualification]
        staffSalaryBase.allowances_coefficient = ALLOWANCE_COEF_DICT[staff.role]
        staffSalaryBase.save()
        return JsonResponse({"staff": ser_instance, "staff_display": staff_display, 'method': 'PUT'}, status=200)
      return JsonResponse({"error": ""}, status=400)
    except IntegrityError as e:
        error_cause = []
        if 'staff_id' in e.args[0]:
          error_cause.append("Staff ID")
        if 'card_id' in e.args[0]:
          error_cause.append("Card ID")
        return JsonResponse({"result": "error","error": f"{', '.join(error_cause)} existed, please try another.", 'method': 'POST'}, status=200)
  def delete(self, *args, **kwargs):
    staff = Staff.objects.get(pk=int(self.request.POST['dindex']))
    ser_instance = serializers.serialize('json', [ staff, ])
    staff.delete()
    return JsonResponse({"staff": ser_instance, 'result': 'success', 'method': 'DELETE'}, status=200)

@login_required
def staff_detail(request, pk):
  staff = Staff.objects.get(pk=pk)
  context = {
    "staff": staff,
  }
  return render(request, "staff_detail.html", context)

@login_required
def search(request, mod):
  if request.method == 'POST' and request.is_ajax() and mod == 'staff':
    search_data = request.POST.get('search_data')
    staffs = Staff.objects.filter(Q(staff_id__contains=search_data) | Q(staff_name__contains=search_data))
    serializedStaffs = []
    serializedStaffs_display = []
    for staff in staffs:
      ser_instance = serializers.serialize('json', [ staff, ])
      display_staff = {
        'role': staff.get_role_display(),
        'department': staff.get_department_display(),
      }
      serializedStaffs.append(ser_instance)
      serializedStaffs_display.append(display_staff)
    
    return JsonResponse({"staffs": serializedStaffs, 'staffs_display': serializedStaffs_display}, status=200)
  if request.method == 'POST' and request.is_ajax() and mod == 'candidate':
    search_data = request.POST.get('search_data')
    candidates = Candidate.objects.filter(Q(c_name__contains=search_data))
    serializedCandidates = []
    for candidate in candidates:
      ser_instance = serializers.serialize('json', [ candidate, ])
      serializedCandidates.append(ser_instance)
    
    return JsonResponse({"candidates": serializedCandidates}, status=200)

@login_required
def recruitment_management(request):
  recruitments = Recruitment.objects.all()
  context = {
    "recruitments": recruitments,
    "form": RecruitmentForm,
  }
  return render(request, 'recruitment_management.html', context)

@login_required
def recruitment_detail(request, pk):
  recruitment = Recruitment.objects.get(pk=pk)
  initValue = {
    'rec_name': recruitment.rec_name,
    'positions': recruitment.positions,
    'quantity': recruitment.quantity,
    'describe': recruitment.describe,
    'requirements': recruitment.requirements,
  }
  form = RecruitmentForm(initial=initValue)
  context = {
    "recruitment": recruitment,
    "form": form,
  }
  return render(request, 'recruitment_detail.html', context)

class RecruitmentManagementView(View):
  http_method_names = ['GET', 'POST', 'PUT', 'DELETE']
  def dispatch(self, *args, **kwargs):
    if self.request.POST:
      if self.request.POST.get('_method') == "POST":
        return self.post(*args, **kwargs)
      elif self.request.POST.get('_method') == "PUT":
        return self.put(*args, **kwargs)
      elif self.request.POST.get('_method') == "DELETE":
        return self.delete(*args, **kwargs)
    return super().dispatch(self.request, *args, **kwargs)
  def post(self, *args, **kwargs):
    form = RecruitmentForm(self.request.POST)
    if form.is_valid():
      recruitment = Recruitment()
      recruitment.rec_name = form.cleaned_data["rec_name"]
      recruitment.positions = form.cleaned_data["positions"]
      recruitment.quantity = form.cleaned_data["quantity"]
      recruitment.describe = form.cleaned_data["describe"]
      recruitment.requirements = form.cleaned_data["requirements"]
      recruitment.save()
      return redirect(reverse("recruitment_management"))
    
  def put(self, *args, **kwargs):
    form = RecruitmentForm(self.request.POST)
    pk = int(self.request.POST.get("index"))
    if form.is_valid():
      recruitment = Recruitment.objects.get(pk=pk)
      recruitment.rec_name = form.cleaned_data["rec_name"]
      recruitment.positions = form.cleaned_data["positions"]
      recruitment.quantity = form.cleaned_data["quantity"]
      recruitment.describe = form.cleaned_data["describe"]
      recruitment.requirements = form.cleaned_data["requirements"]
      recruitment.save()
      return redirect(reverse("recruitment_detail", args=(pk,)))
  def delete(self, *args, **kwargs):
    recruitment = Recruitment.objects.get(pk=int(self.request.POST.get("index")))
    recruitment.delete()
    return redirect(reverse("recruitment_management"))

@login_required
def recruitment_candidate(request, pk):
  recruitment = Recruitment.objects.get(pk=pk)
  form = CandidateForm()
  context = {
    'recruitment': recruitment,
    'form': form,
  }
  return render(request, 'recruitment_candidate.html', context)

class CandidateAjaxView(View):
  http_method_names = ['GET', 'POST', 'PUT', 'DELETE']
  def dispatch(self, *args, **kwargs):
    if self.request.is_ajax() and self.request.POST:
      if self.request.POST.get('_method') == "POST":
        return self.post(*args, **kwargs)
      elif self.request.POST.get('_method') == "PUT":
        return self.put(*args, **kwargs)
      elif self.request.POST.get('_method') == "DELETE":
        return self.delete(*args, **kwargs)
    return super().dispatch(self.request, *args, **kwargs)

  def post(self, *args, **kwagrs):
    try:
      form = CandidateForm(self.request.POST)
      if form.is_valid():
        candidate = Candidate()
        candidate.c_name = form.cleaned_data["c_name"]
        candidate.dob = form.cleaned_data["dob"]
        candidate.card_id = form.cleaned_data["card_id"]
        candidate.address = form.cleaned_data["address"]
        candidate.phone = form.cleaned_data["phone"]
        candidate.qualification = form.cleaned_data["qualification"]
        candidate.recruitment = Recruitment.objects.get(pk=int(self.request.POST['rec_index']))
        candidate.save()
        ser_instance = serializers.serialize('json', [ candidate, ])
        return JsonResponse({"candidate": ser_instance, 'method': 'POST'}, status=200)
    except IntegrityError as e:
      return JsonResponse({"result": "error","error": "Card ID existed, please try another.", 'method': 'POST'}, status=200)
      

  def put(self, *args, **kwagrs):
    try:
      form = CandidateForm(self.request.POST)
      if form.is_valid():
        candidate = Candidate.objects.get(pk=int(self.request.POST['index']))
        candidate.c_name = form.cleaned_data["c_name"]
        candidate.dob = form.cleaned_data["dob"]
        candidate.card_id = form.cleaned_data["card_id"]
        candidate.address = form.cleaned_data["address"]
        candidate.phone = form.cleaned_data["phone"]
        candidate.qualification = form.cleaned_data["qualification"]
        candidate.save()
        ser_instance = serializers.serialize('json', [ candidate, ])
        return JsonResponse({"candidate": ser_instance, 'method': 'PUT'}, status=200)
      return JsonResponse({"error": ""}, status=400)
    except IntegrityError as e:
        return JsonResponse({"result": "error","error": "Card ID existed, please try another.", 'method': 'POST'}, status=200)

  def delete(self, *args, **kwargs):
    candidate = Candidate.objects.get(pk=int(self.request.POST['dindex']))
    ser_instance = serializers.serialize('json', [ candidate, ])
    candidate.delete()
    return JsonResponse({"candidate": ser_instance, 'result': 'success', 'method': 'DELETE'}, status=200)
 
@login_required
def salary_management(request):
  context = {
    "months": [x for x in range(1, 13)],
    "years": [2020, 2021],
  }
  if request.GET.get("month"):
    month = int(request.GET.get("month"))
    year = int(request.GET.get("year"))
    monthSalarys = MonthSalary.objects.filter(year=year).filter(month=month)
    context["monthSalarys"] = monthSalarys
    context["month"] = month
    context["year"] = year
  return render(request, "salary_management.html", context)

@login_required
def workday_management(request):
  context = {
    "form": DatePickerForm,
  }
  if request.method == "GET":
    if request.GET.get("date"):
      date = str(request.GET.get("date"))[:11]
      dates = date.split("/")
      day, month, year = int(dates[0]), int(dates[1]), int(dates[2])
      staffs = Staff.objects.all()
      for staff in staffs:
        workday = WorkDay.objects.filter(staff=staff).filter(year=year).filter(month=month).filter(day=day).first()
        if workday is None:
          workday = WorkDay()
          workday.staff = staff
          workday.day = day
          workday.month = month
          workday.year = year
          workday.save()
      workdays = WorkDay.objects.filter(year=year).filter(month=month).filter(day=day)
      context["workdays"] = workdays
      context["day"] = day
      context["month"] = month
      context["year"] = year
    return render(request, "work_day.html", context)
  elif request.method == "POST":
    pk = request.POST.get("pk")
    wday = WorkDay.objects.get(pk=pk)
    start_time = request.POST.get("start_time")
    end_time = request.POST.get("end_time")
    wday.start_time = datetime.strptime(start_time, '%H:%M')
    wday.end_time = datetime.strptime(end_time, '%H:%M')
    wday.save()
    day, month, year = wday.day, wday.month, wday.year
    workdays = WorkDay.objects.filter(year=year).filter(month=month).filter(day=day)
    context["workdays"] = workdays
    context["day"] = day
    context["month"] = month
    context["year"] = year
    return render(request, "work_day.html", context)

def time_keeping(request):
  if request.GET.get("month"):
    print("go")
    month = request.GET.get("month")
    year = request.GET.get("year")
    staffs = Staff.objects.all()
    for staff in staffs:
      monthSalary = MonthSalary.objects.filter(staff=staff).filter(year=year).filter(month=month).first()
      if monthSalary is None:
        monthSalary = MonthSalary()
        monthSalary.staff = staff
        monthSalary.month = month
        monthSalary.year = year
      total_time = 0
      workdays = WorkDay.objects.filter(staff=staff).filter(year=year).filter(month=month)
      for workday in workdays:
        t1 = workday.start_time.strftime("%H:%M")
        t2 = datetime.strptime(t1, '%H:%M')
        t3 = workday.end_time.strftime("%H:%M")
        t4 = datetime.strptime(t3, '%H:%M')
        dur = t4 - t2
        total_time += round((dur.seconds/3600), 2)
      monthSalary.administrative = total_time
      monthSalary.overtime = 0
      monthSalary.dayoff = 0
      monthSalary.holiday = 0
      monthSalary.save()
  
  return redirect(reverse("salary_management"))