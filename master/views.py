from django.shortcuts import render

from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

from django.utils.decorators import method_decorator
from django.shortcuts import redirect, HttpResponseRedirect, get_object_or_404

from django.urls import reverse_lazy
from django.http import JsonResponse, Http404, HttpResponse

from django.db.models import Sum

from django_tables2.export.views import ExportMixin
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from college.settings import engine

from users.models import *
from users.forms import *
from .forms import *
from .tables import  *
from users.choices import PAYMENT_STATUS
import csv
from django_tables2 import SingleTableView

@method_decorator(staff_member_required, name='dispatch')
class AddBoard(CreateView, SingleTableView):
	table_class = BoardListTable
	model = Board
	fields = ('name', 'status')
	template_name = 'registration/create_form.html'
	success_url = reverse_lazy('master:add_board')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Add Board'
		context['list_title'] = 'Board List'
		context['list_id'] = 'add_board'
		return context

@method_decorator(staff_member_required, name="dispatch")
class UpdateBoard(UpdateView, SingleTableView):
	table_class = BoardListTable
	model = Board
	fields = '__all__'
	template_name = 'registration/create_form.html'
	success_url = reverse_lazy('master:add_board')

	def get_queryset(self):
		return self.model.objects.filter().exclude(pk=self.kwargs['pk'])

	def get_object(self):
		return self.model.objects.get(pk=self.kwargs['pk'])

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Add Board'
		context['list_title'] = 'Board List'
		context['list_id'] = 'add_board'
		return context


@method_decorator(staff_member_required, name='dispatch')
class AddCourse(CreateView, SingleTableView):
	table_class = CourseListTable
	model = Courses
	fields = '__all__'
	template_name = 'registration/create_form.html'
	success_url = reverse_lazy('master:add_course')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Add Course'
		context['list_title'] = 'Course List'
		context['list_id'] = 'add_course'
		return context

@method_decorator(staff_member_required, name="dispatch")
class UpdateCourse(UpdateView, SingleTableView):
	table_class = CourseListTable
	model = Courses
	fields = '__all__'
	template_name = 'registration/create_form.html'
	success_url = reverse_lazy('master:add_course')

	def get_queryset(self):
		return self.model.objects.filter().exclude(pk=self.kwargs['pk'])

	def get_object(self):
		return self.model.objects.get(pk=self.kwargs['pk'])

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Add Course'
		context['list_title'] = 'Course List'
		context['list_id'] = 'add_course'
		return context


@method_decorator(staff_member_required, name='dispatch')
class AddSubject(CreateView, SingleTableView):
	table_class = SubjectListTable
	model = Subject
	fields = '__all__'
	template_name = 'registration/create_form.html'
	success_url = reverse_lazy('master:add_subject')

	def get_table_template(self):
		return "registration/"+self.model.__name__.lower()+"_table.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['object_list'] = self.model.objects.all()
		context['title'] = 'Add Subject'
		context['list_title'] = 'Subject List'
		context['table_template'] = self.get_table_template()
		context['list_id'] = 'add_subject'
		return context

@method_decorator(staff_member_required, name="dispatch")
class UpdateSubject(UpdateView, SingleTableView):
	table_class = SubjectListTable
	model = Subject
	fields = '__all__'
	template_name = 'registration/create_form.html'
	success_url = reverse_lazy('master:add_subject')

	def get_queryset(self):
		return self.model.objects.filter().exclude(pk=self.kwargs['pk'])

	def get_object(self):
		return self.model.objects.get(pk=self.kwargs['pk'])

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Add Subject'
		context['list_title'] = 'Subject List'
		context['list_id'] = 'add_subject'
		return context


@method_decorator(staff_member_required, name='dispatch')
class AddPSubject(CreateView, SingleTableView):
	table_class = PSubjectListTable
	form_class = PsubjectForm
	model = practical
	template_name = 'registration/create_form.html'
	success_url = reverse_lazy('master:add_psubject')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Add Practical Subject'
		context['list_title'] = 'Practical  Subject List'
		context['list_id'] = 'add_psubject'
		return context

@method_decorator(staff_member_required, name="dispatch")
class UpdatePSubject(UpdateView, SingleTableView):
	table_class = PSubjectListTable
	model = practical
	form_class = PsubjectForm
	template_name = 'registration/create_form.html'
	success_url = reverse_lazy('master:add_psubject')

	def get_queryset(self):
		return self.model.objects.filter().exclude(pk=self.kwargs['pk'])

	def get_object(self):
		return self.model.objects.get(pk=self.kwargs['pk'])

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Add Practical Subject'
		context['list_title'] = 'Practical Subject List'
		context['list_id'] = 'add_psubject'
		return context

@method_decorator(staff_member_required, name='dispatch')
class AddSession(CreateView, SingleTableView):
	table_class = SessionListTable
	model = Session
	fields = '__all__'
	template_name = 'registration/create_form.html'
	success_url = reverse_lazy('master:add_session')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Add Session'
		context['list_title'] = 'Session List'
		context['list_id'] = 'add_session'
		return context

@method_decorator(staff_member_required, name="dispatch")
class UpdateSession(UpdateView, SingleTableView):
	model = Session
	fields = '__all__'
	template_name = 'registration/create_form.html'
	success_url = reverse_lazy('master:add_session')

	def get_queryset(self):
		return self.model.objects.filter().exclude(pk=self.kwargs['pk'])

	def get_object(self):
		return self.model.objects.get(pk=self.kwargs['pk'])

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Add Session'
		context['list_title'] = 'Session List'
		context['list_id'] = 'add_session'
		return context

@method_decorator(staff_member_required, name='dispatch')
class AddComposition(CreateView, SingleTableView):
	table_class = CompositionListTable
	model = Composition
	fields = '__all__'
	template_name = 'registration/create_form.html'
	success_url = reverse_lazy('master:add_composition')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Add Composition'
		context['list_title'] = 'Composition List'
		context['list_id'] = 'add_composition'
		return context

@method_decorator(staff_member_required, name="dispatch")
class UpdateComposition(UpdateView, SingleTableView):
	table_class = CompositionListTable
	model = Composition
	fields = '__all__'
	template_name = 'registration/create_form.html'
	success_url = reverse_lazy('master:add_composition')

	def get_queryset(self):
		return self.model.objects.filter().exclude(pk=self.kwargs['pk'])

	def get_object(self):
		return self.model.objects.get(pk=self.kwargs['pk'])

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Add Composition'
		context['list_title'] = 'Composition List'
		context['list_id'] = 'add_composition'
		return context


@method_decorator(staff_member_required, name='dispatch')
class AddFee(SuccessMessageMixin, CreateView, SingleTableView):
	table_class = FeeMasterListTable
	model = FeeMaster
	# fields = '__all__'
	form_class = AddFeeForm
	template_name = 'master/add_fee.html'
	success_url = reverse_lazy('master:add_fee')
	success_message = 'Course :- %(course)s, Feehead :- %(feehead)s, Gender :- %(gender)s, Board :- %(board)s Fee successfully added for all category'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Add Fee'
		context['list_title'] = 'Fee List'
		context['list_id'] = 'add_fee'
		return context

@method_decorator(staff_member_required, name="dispatch")
class UpdateFee(SuccessMessageMixin, UpdateView, SingleTableView):
	table_class = FeeMasterListTable
	model = FeeMaster
	form_class = UpdateFeeForm
	template_name = 'registration/create_form.html'
	success_url = reverse_lazy('master:add_fee')
	success_message = 'Fee Structure Successfully Updated'

	def get_queryset(self):
		return self.model.objects.filter().exclude(pk=self.kwargs['pk'])

	def get_object(self):
		return self.model.objects.get(pk=self.kwargs['pk'])

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Add Fee'
		context['list_title'] = 'Fee List'
		context['list_id'] = 'add_fee'
		return context

@staff_member_required
def EditProfile(request):
	form = SearchStudent(request.POST or None)
	context = {
		"form": form
	}
	if request.method == 'POST':
		try:
			context['table'] = StudentTable(Profile.objects.filter(user__username__contains=request.POST.get('username')))
		except Exception as e:
			print(e)
			form.add_error('username', 'No User Found {}'.format(request.POST.get('username')))
	return render(request, 'registration/create_form.html', context)

@method_decorator(staff_member_required, name="dispatch")
class UpdateStudentProfile(UpdateView):
	model = Profile
	fields = '__all__'
	template_name = 'master/student-basic.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['by_admin'] = True
		return context

	def get_success_url(self):
		print(self.object)
		return reverse_lazy('master:update_student_education', kwargs={'pk': self.object.user.id})


@staff_member_required
def UpdateStudentEducation(request, pk):
	user = User.objects.get(pk=pk)
	if hasattr(user, 'previouseducation'):
		form = StudentEducationForms(request.POST or None, request.FILES or None, instance=user.profile.previouseducation)
	else:
		form = StudentEducationForms(request.POST or None, request.FILES or None)
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse_lazy("master:update_student_education", kwargs={'pk': user.id}))
	context = {"form": form, "student": user}
	return render(request, 'master/student_education.html', context)

@method_decorator(staff_member_required, name="dispatch")
class UpdateEducationDetail(UpdateView):
	model = PreviousEducation
	template_name = 'master/student_education.html'
	fields = '__all__'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['student'] = User.objects.get(pk=self.kwargs['user_id'])
		context['update'] = True
		return context

	def get_success_url(self):
		return reverse_lazy('master:update_student_education', kwargs={'pk': self.kwargs['user_id']})


@staff_member_required
def StudentCourse(request, pk):
	user = User.objects.get(pk=pk)
	if not user.profile.previouseducation_set.all():
		return redirect(reverse_lazy("master:update_student_education", kwargs={'pk': pk}))
	if hasattr(user.profile, 'coursedetail'):
		form = StudentCourseExist(request.POST or None, instance=user.profile.coursedetail)
	else:
		form = StudentCourseForms(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse_lazy("master:course_detail", kwargs={'pk': pk}))
	context = {"form": form, 'student': user}
	return render(request, 'master/student_course.html', context)


@method_decorator(staff_member_required, name="dispatch")
class AddStudent(SuccessMessageMixin, CreateView):
	form_class = AddStudentForm
	template_name = 'master/profile_form.html'
	success_url = reverse_lazy('master:add_student')
	success_message = "%(first_name)s %(last_name)s with %(reg_no)s was created successfully"


@method_decorator(staff_member_required, name="dispatch")
class AddBulkStudent(SuccessMessageMixin, CreateView):
	form_class = AddBulkStudent
	template_name = 'master/profile_form.html'
	success_url = reverse_lazy('master:add_bstudent')
	success_message = 'Data successfully created'

@method_decorator(staff_member_required, name="dispatch")
class PaidStudentReport(SingleTableMixin, FilterView):
    table_class = PaidStudentTable
    model = PaymentStatus
    template_name = "master/paid.html"

    filterset_class = PaidStudentFilter
    queryset = model.objects.filter(status=1, profile__clc_status=False)

    def get_context_data(self, **kwargs):
    	context = super().get_context_data(**kwargs)
    	context['CLC_False'] = True
    	return context

@staff_member_required
def PaidReportDownload(request):
	kwargs = request.GET.copy()
	filters = {'profile__clc_status': False}
	for i,j in kwargs.items():
		if kwargs[i]:
			filters[i] = j
	filters.pop('page', None)
	print(filters)
	ren = {'f_name': 'Father Name', 'm_name': 'Mother Name'}
	data = pd.read_sql("""SELECT reg_no, CONCAT(first_name, ' ', last_name) as full_name, email, f_name, m_name, 
				gender, dob, m_status, adhar, phone, 
				whatsapp, address, state, city, district, pincode, religion, 
				category, g_occupation, g_income, phy_disabled, merit,
				last_session, inter_marks, inter_roll_code, inter_roll_no, 
				comp_paper_id, course_id, enroll_session_id, hons_paper_id, 
				sub1_paper_id, sub2_paper_id, amount, easepayid, TO_CHAR(created_at, 'DD/MM/YYYY HH:MI am') as Payment_At
				FROM public.users_profile as pf inner join users_coursedetail as cd on pf.id=cd.profile_id
				inner join users_paymentstatus as ps on ps.profile_id=pf.id
				inner join auth_user as users on pf.user_id=users.id
				where ps.status=1;""", engine, index_col="reg_no")
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename=filename.csv'
	data['gender'] = data['gender'].map(dict((x, y) for x, y in GENDER))
	data['religion'] = data['religion'].map(dict((x, y) for x, y in RELIGION_LIST))
	data['m_status'] = data['m_status'].map(dict((x, y) for x, y in MARITAL_STATUS))
	data['category'] = data['category'].map(dict((x, y) for x, y in CATEGORY))
	data['phy_disabled'] = data['phy_disabled'].map(dict((x, y) for x, y in DISABLED))
	data['merit'] = data['merit'].map(dict((x, y) for x, y in MERIT_LIST_CHOICES))
	sub = {i.pk:i.name for i in Subject.objects.all()}
	comp = {i.pk:i.sub.name for i in Composition.objects.all()}
	session = {i.pk:i.name for i in Session.objects.all()}
	data['hons_paper_id'] = data['hons_paper_id'].map(sub)
	data['sub1_paper_id'] = data['sub1_paper_id'].map(sub)
	data['sub2_paper_id'] = data['sub2_paper_id'].map(sub)
	data['comp_paper_id'] = data['comp_paper_id'].map(comp)
	data['enroll_session_id'] = data['enroll_session_id'].map(session)
	data['course_id'] = data['course_id'].map({i.pk:i.name for i in Courses.objects.all()})
	data.rename(columns=ren, inplace=True)
	d = {}
	for i in data.columns:
		if i.endswith('_id'):
			d[i] = i[:-3]
	data.rename(columns=d, inplace=True)
	data.to_csv(path_or_buf=response,sep=';',float_format='%.2f')
	return response

@method_decorator(staff_member_required, name="dispatch")
class PaidCLCReport(ExportMixin, SingleTableMixin, FilterView):
    table_class = PaidCLCTable
    model = PaymentStatus
    template_name = "master/paid.html"

    filterset_class = PaidCLCFilter
    queryset = model.objects.filter(status=1, profile__clc_status=True)

@staff_member_required
def PaidCLCDownload(request):
	kwargs = request.GET.copy()
	filters = {'profile__clc_status': False}
	for i,j in kwargs.items():
		if kwargs[i]:
			filters[i] = j
	filters.pop('page', None)
	ren = {'f_name': 'Father Name', 'm_name': 'Mother Name'}
	data = pd.read_sql("""SELECT reg_no, CONCAT(first_name, ' ', last_name) as full_name, email, 
		f_name, m_name, gender, dob, m_status, adhar, phone, 
		whatsapp, address, state, city, district, pincode, religion,
		category, g_occupation, g_income, phy_disabled,
		exm_roll, cls_roll, exm_year, pass_year, total_marks, obtained_marks, 
		division, exm_month, course_id, session_id, fee_type, easepayid, amount as Fee, TO_CHAR(created_at, 'DD/MM/YYYY HH:MI am') as Payment_At
		FROM public.users_profile as pf inner join users_paymentstatus as ps on ps.profile_id=pf.id
		inner join users_clcstudent as clc on clc.profile_id=pf.id
		inner join auth_user as users on users.id=pf.user_id
		where pf.clc_status=true and ps.status=1;
		""", engine, index_col="reg_no")
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename=filename.csv'
	data['gender'] = data['gender'].map(dict((x, y) for x, y in GENDER))
	data['religion'] = data['religion'].map(dict((x, y) for x, y in RELIGION_LIST))
	data['m_status'] = data['m_status'].map(dict((x, y) for x, y in MARITAL_STATUS))
	data['category'] = data['category'].map(dict((x, y) for x, y in CATEGORY))
	data['fee_type'] = data['fee_type'].map(dict((x, y) for x, y in CLC_FEE_TYPE))
	data['phy_disabled'] = data['phy_disabled'].map(dict((x, y) for x, y in DISABLED))
	data['course_id'] = data['course_id'].map({i.pk:i.name for i in Courses.objects.all()})
	data['session_id'] = data['session_id'].map({i.pk:i.name for i in CLCYear.objects.all()})
	data.rename(columns=ren, inplace=True)
	d = {}
	for i in data.columns:
		if i.endswith('_id'):
			d[i] = i[:-3]
	data.rename(columns=d, inplace=True)
	data.to_csv(path_or_buf=response,sep=';',float_format='%.2f')
	return response


@method_decorator(staff_member_required, name="dispatch")
class AddClcFee(SuccessMessageMixin, CreateView, SingleTableView):
	table_class = CLCFeeListTable
	model = CLCFee
	fields = '__all__'
	template_name = 'registration/create_form.html'
	success_url = reverse_lazy('master:add_clc_fee')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Add CLC Fee'
		context['list_title'] = 'CLC Fee List'
		context['list_id'] = 'add_clc'
		return context

@method_decorator(staff_member_required, name="dispatch")
class UpdateCLCFee(UpdateView, SingleTableView):
	table_class = CLCFeeListTable
	model = CLCFee
	fields = '__all__'
	template_name = 'registration/create_form.html'
	success_url = reverse_lazy('master:add_clc_fee')
	success_message = 'Fee Structure Successfully Updated'

	def get_queryset(self):
		return self.model.objects.filter().exclude(pk=self.kwargs['pk'])

	def get_object(self):
		return self.model.objects.get(pk=self.kwargs['pk'])

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Add CLC Fee'
		context['list_title'] = 'CLC FEE List'
		context['list_id'] = 'add_clc'
		return context