from django.urls import path, include

from .views import *

app_name="college"

urlpatterns = [
	path('register/', Register, name="register"),
	path('dashboard/', Dashboard, name="college_dashboard"),
	path('get_subjects/', getSubjects, name="get_subjects"),
	path('StudentBasicInfo/', StudentBasicInfo.as_view(), name="student_basic"),
	path('StudentEducationDetails/', StudentEducationDetails, name="student_education"),
	path('StudentEducationDetailsUpdate/<int:pk>/', StudentEducationUpdate.as_view(), name="student_education_update"),
	path('StudentCourseDetails/', StudentCourseDetails, name="student_course"),
	path('StudentDetailsPreview/', StudentDetailsPreview.as_view(), name="student_course_preview"),
	path('PaymentInit/', PaymentInit, name="PaymentInit"),
	path('PaymentReceipt/', PaymentReceipt, name="PaymentReceipt"),
	path('PaymentConfirmation/', PaymentConfirmation, name="PaymentConfirmation"),

]