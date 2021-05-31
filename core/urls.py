from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('search/<str:mod>', views.search, name='search'),
  path('profile_management/', views.profile_management, name='profile_management'),
  path('profile_management/<int:pk>/staff_detail', views.staff_detail, name='staff_detail'),
  path('profile_management_ajax/', views.ProfileManagementAjaxView.as_view(), name='profile_management_ajax'),
  path('recruitment_management/', views.recruitment_management, name="recruitment_management"),
  path('recruitment/actions', views.RecruitmentManagementView.as_view(), name="recruitment"),
  path('recruitment/<int:pk>', views.recruitment_detail, name="recruitment_detail"),
  path('recruitment/<int:pk>/candidates', views.recruitment_candidate, name="recruitment_candidate"),
  path('candidate/actions', views.CandidateAjaxView.as_view(), name="candidate_ajax"),
  path('salary_management/', views.salary_management, name="salary_management"),
  path('workday_management/', views.workday_management, name="workday_management"),
  path('time_keeping/', views.time_keeping, name="time_keeping"),
]