from django.urls import path, include

from .views import *

app_name="master"

urlpatterns = [
	path('addBoard/', AddBoard.as_view(), name="add_board"),
	path('updateBoard/<int:pk>/', UpdateBoard.as_view(), name="update_board"),
	path('addCourse/', AddCourse.as_view(), name="add_course"),
	path('updateCoure/<int:pk>/', UpdateCourse.as_view(), name="update_course"),
	path('addSubject/', AddSubject.as_view(), name="add_subject"),
	path('addPSubject/', AddPSubject.as_view(), name="add_psubject"),
	path('updateSubject/<int:pk>/', UpdateSubject.as_view(), name="update_subject"),
	path('updatePSubject/<int:pk>/', UpdatePSubject.as_view(), name="update_psubject"),
	path('addSession/', AddSession.as_view(), name="add_session"),
	path('updateSession/<int:pk>/', UpdateSession.as_view(), name="update_session"),
	path('addComposition/', AddComposition.as_view(), name="add_composition"),
	path('updateComposition/<int:pk>/', UpdateComposition.as_view(), name="update_composition"),
	path('addFee/', AddFee.as_view(), name="add_fee"),
	path('updateFee/<int:pk>/', UpdateFee.as_view(), name="update_fee"),
	path('addClcFee/', AddClcFee.as_view(), name="add_clc_fee"),
	path('updateClcFee/<int:pk>/', UpdateCLCFee.as_view(), name="update_clc_fee"),
	path('EditProfile/', EditProfile, name="edit_profile"),
	path('UpdateStudentProfile/<int:pk>/', UpdateStudentProfile.as_view(), name="update_student"),
	path('UpdateStudentEducation/<int:pk>/', UpdateStudentEducation, name="update_student_education"),
	path('UpdateEducationDetail/<int:pk>/<int:user_id>', UpdateEducationDetail.as_view(), name="update_education_detail"),
	path('StudentCourse/<int:pk>/', StudentCourse, name="course_detail"),
	path('AddStudent/', AddStudent.as_view(), name="add_student"),
	path('AddBulkStudent/', AddBulkStudent.as_view(), name="add_bstudent"),
	path('PaidStudentReport/', PaidStudentReport.as_view(), name="paid_student_report"),
	path('PaidReportDownload/', PaidReportDownload, name="PaidReportDownload"),
	path('PaidCLCReport/', PaidCLCReport.as_view(), name="paid_clc_report"),
	path('PaidCLCDownload/', PaidCLCDownload, name="PaidCLCDownload"),
]