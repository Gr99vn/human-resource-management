from django import forms
from django.forms.widgets import SelectDateWidget

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

class StaffForm(forms.Form):
  staff_id = forms.CharField(required=True, 
    widget=forms.TextInput(
      attrs={
        'class': 'form-control',
      }
    )
  )
  staff_name = forms.CharField(widget=forms.TextInput(
    attrs={
      'class': 'form-control',
    })
  )
  role = forms.ChoiceField(choices=ROLE_CHOICES,
    widget=forms.Select(
    attrs={
      'class': 'form-control',
    }) 
  )
  phone = forms.CharField(widget=forms.TextInput(
    attrs={
      'class': 'form-control',
    })
  )
  card_id = forms.CharField(widget=forms.TextInput(
    attrs={
      'class': 'form-control',
    })
  )
  address = forms.CharField(widget=forms.TextInput(
    attrs={
      'class': 'form-control',
    })
  )
  department = forms.ChoiceField(choices=DEPARTMENT_CHOICES,
    widget=forms.Select(
    attrs={
      'class': 'form-control',
    })
  )
  qualification = forms.ChoiceField(choices=QUALIFICATION_CHOICES,
    widget=forms.Select(
    attrs={
      'class': 'form-control',
    })
  )

class RecruitmentForm(forms.Form):
  rec_name = forms.CharField(widget=forms.TextInput(
    attrs={
      'class': 'form-control',
    })
  )
  positions = forms.CharField(widget=forms.TextInput(
    attrs={
      'class': 'form-control',
    }
  ))
  describe = forms.CharField(widget=forms.Textarea(
    attrs={
      "class": "form-control",
      "rows":5, 
      "cols":30    
    }
  ))
  quantity = forms.IntegerField(widget=forms.NumberInput(
    attrs={
      'class': 'form-control',
    }
  ))
  requirements = forms.CharField(widget=forms.Textarea(
    attrs={
      "class": "form-control",
      "rows":5, 
      "cols":30    
    }
  ))

class CandidateForm(forms.Form):
  c_name = forms.CharField(
    required=True, 
    widget=forms.TextInput(attrs={
      'class': 'form-control'
    })
  )
  dob = forms.DateField(
    input_formats=['%d/%m/%Y'],
    widget=forms.DateInput(attrs={
      'class': 'form-control d-inline datetimepicker-input',
      'data-target': '#id_dob',
      'size': 10,
      'style': 'width:90%;'
    })
  )
  phone = forms.CharField(
    widget=forms.TextInput(attrs={
      'class': 'form-control'
    })
  )
  card_id = forms.CharField(
    widget=forms.TextInput(attrs={
      'class': 'form-control'
    })
  )
  address = forms.CharField(
    widget=forms.TextInput(attrs={
      'class': 'form-control'
    })
  )
  qualification = forms.CharField(
    widget=forms.TextInput(attrs={
      'class': 'form-control'
    })
  )

class DatePickerForm(forms.Form):
  date = forms.DateField(
    input_formats=['%d/%m/%Y'],
    widget=forms.DateInput(attrs={
      'class': 'form-control d-inline datetimepicker-input',
      'data-target': '#id_date',
      'size': 10,
      'style': 'width:10%;'
    })
  )