from django.shortcuts import render

from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic.base import TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin

from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, HttpResponseRedirect, get_object_or_404

from django.urls import reverse_lazy
from django.http import JsonResponse, Http404, HttpResponse

from django.db.models import Sum

from users.models import *
from users.forms import *
from .forms import *

@method_decorator(staff_member_required, name='dispatch')
class AddBoard(CreateView):
	model = Board
	fields = '__all__'
	template_name = 'registration/create_form.html'
	success_url = reverse_lazy('master:add_board')

	def get_table_template(self):
		return "registration/"+self.model.__name__.lower()+"_table.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['object_list'] = self.model.objects.all()
		context['title'] = 'Add Board'
		context['list_title'] = 'Board List'
		context['table_template'] = self.get_table_template()
		context['list_id'] = 'add_board'
		return context

@method_decorator(staff_member_required, name="dispatch")
class UpdateBoard(UpdateView):
	model = Board
	fields = '__all__'
	template_name = 'registration/create_form.html'
	success_url = reverse_lazy('master:add_board')

	def get_table_template(self):
		return "registration/"+self.model.__name__.lower()+"_table.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['object_list'] = self.model.objects.filter().exclude(pk=self.kwargs['pk'])
		context['title'] = 'Add Board'
		context['list_title'] = 'Board List'
		context['table_template'] = self.get_table_template()
		context['list_id'] = 'add_board'
		return context


@method_decorator(staff_member_required, name='dispatch')
class AddCourse(CreateView):
	model = Courses
	fields = '__all__'
	template_name = 'registration/create_form.html'
	success_url = reverse_lazy('master:add_course')

	def get_table_template(self):
		return "registration/"+self.model.__name__.lower()+"_table.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['object_list'] = self.model.objects.all()
		context['title'] = 'Add Course'
		context['list_title'] = 'Course List'
		context['table_template'] = self.get_table_template()
		context['list_id'] = 'add_course'
		return context

@method_decorator(staff_member_required, name="dispatch")
class UpdateCourse(UpdateView):
	model = Courses
	fields = '__all__'
	template_name = 'registration/create_form.html'
	success_url = reverse_lazy('master:add_course')

	def get_table_template(self):
		return "registration/"+self.model.__name__.lower()+"_table.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['object_list'] = self.model.objects.filter().exclude(pk=self.kwargs['pk'])
		context['title'] = 'Add Course'
		context['list_title'] = 'Course List'
		context['table_template'] = self.get_table_template()
		context['list_id'] = 'add_course'
		return context


@method_decorator(staff_member_required, name='dispatch')
class AddSubject(CreateView):
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
class UpdateSubject(UpdateView):
	model = Subject
	fields = '__all__'
	template_name = 'registration/create_form.html'
	success_url = reverse_lazy('master:add_subject')

	def get_table_template(self):
		return "registration/"+self.model.__name__.lower()+"_table.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['object_list'] = self.model.objects.filter().exclude(pk=self.kwargs['pk'])
		context['title'] = 'Add Subject'
		context['list_title'] = 'Subject List'
		context['table_template'] = self.get_table_template()
		context['list_id'] = 'add_subject'
		return context

@method_decorator(staff_member_required, name='dispatch')
class AddSession(CreateView):
	model = Session
	fields = '__all__'
	template_name = 'registration/create_form.html'
	success_url = reverse_lazy('master:add_session')

	def get_table_template(self):
		return "registration/"+self.model.__name__.lower()+"_table.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['object_list'] = self.model.objects.all()
		context['title'] = 'Add Session'
		context['list_title'] = 'Session List'
		context['table_template'] = self.get_table_template()
		context['list_id'] = 'add_session'
		return context

@method_decorator(staff_member_required, name="dispatch")
class UpdateSession(UpdateView):
	model = Session
	fields = '__all__'
	template_name = 'registration/create_form.html'
	success_url = reverse_lazy('master:add_session')

	def get_table_template(self):
		return "registration/"+self.model.__name__.lower()+"_table.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['object_list'] = self.model.objects.filter().exclude(pk=self.kwargs['pk'])
		context['title'] = 'Add Session'
		context['list_title'] = 'Session List'
		context['table_template'] = self.get_table_template()
		context['list_id'] = 'add_session'
		return context

@method_decorator(staff_member_required, name='dispatch')
class AddComposition(CreateView):
	model = Composition
	fields = '__all__'
	template_name = 'registration/create_form.html'
	success_url = reverse_lazy('master:add_composition')

	def get_table_template(self):
		return "registration/"+self.model.__name__.lower()+"_table.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['object_list'] = self.model.objects.all()
		context['title'] = 'Add Composition'
		context['list_title'] = 'Composition List'
		context['table_template'] = self.get_table_template()
		context['list_id'] = 'add_composition'
		return context

@method_decorator(staff_member_required, name="dispatch")
class UpdateComposition(UpdateView):
	model = Composition
	fields = '__all__'
	template_name = 'registration/create_form.html'
	success_url = reverse_lazy('master:add_composition')

	def get_table_template(self):
		return "registration/"+self.model.__name__.lower()+"_table.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['object_list'] = self.model.objects.filter().exclude(pk=self.kwargs['pk'])
		context['title'] = 'Add Composition'
		context['list_title'] = 'Composition List'
		context['table_template'] = self.get_table_template()
		context['list_id'] = 'add_composition'
		return context


@method_decorator(staff_member_required, name='dispatch')
class AddFee(CreateView):
	model = FeeMaster
	fields = '__all__'
	template_name = 'registration/create_form.html'
	success_url = reverse_lazy('master:add_fee')

	def get_table_template(self):
		return "registration/"+self.model.__name__.lower()+"_table.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['object_list'] = self.model.objects.all()
		context['title'] = 'Add Fee'
		context['list_title'] = 'Fee List'
		context['table_template'] = self.get_table_template()
		context['list_id'] = 'add_fee'
		return context

@method_decorator(staff_member_required, name="dispatch")
class UpdateFee(UpdateView):
	model = FeeMaster
	fields = '__all__'
	template_name = 'registration/create_form.html'
	success_url = reverse_lazy('master:add_fee')

	def get_table_template(self):
		return "registration/"+self.model.__name__.lower()+"_table.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['object_list'] = self.model.objects.filter().exclude(pk=self.kwargs['pk'])
		context['title'] = 'Add Fee'
		context['list_title'] = 'Fee List'
		context['table_template'] = self.get_table_template()
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
			print(request.POST.get('username'))
			context['student'] = User.objects.get(username=request.POST.get('username')).profile
			context['table_template'] = 'registration/student_search.html'
			context['object_list'] = True
		except Exception as e:
			print(e)
			form.add_error('username', 'No User Found {}'.format(request.POST.get('username')))
	print(context)
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
class AddBulkStudent(SuccessMessageMixin, FormView):
	form_class = AddBulkStudent
	template_name = 'master/profile_form.html'
	success_url = reverse_lazy('master:add_bstudent')
	success_message = 'Data successfully created'