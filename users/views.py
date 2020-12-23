from django.shortcuts import render

from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, HttpResponseRedirect, get_object_or_404

from django.urls import reverse_lazy
from django.http import JsonResponse, Http404, HttpResponse

from django.db.models import Sum
from datetime import date

from .models import *
from .forms import *

@login_required
def Dashboard(request):
	print(request.user.is_staff)
	if request.user.is_staff:
		return render(request, 'student/dashboard.html', {})
	return render(request, 'student/dashboard1.html', {})


class StudentBasicInfo(LoginRequiredMixin, UpdateView):
	form_class = StudentForms
	template_name = 'student/student_basic.html'
	success_url = reverse_lazy("college:student_education")

	def get_object(self):
		return self.request.user.profile

	def get_form_kwargs(self):
	    kwargs = super(StudentBasicInfo, self).get_form_kwargs()
	    kwargs.update({'user': self.request.user})
	    return kwargs

@login_required
def StudentEducationDetails(request):
	if hasattr(request.user.profile, 'previouseducation'):
		form = StudentEducationForms(request.POST or None, request.FILES or None, instance=request.user.profile.previouseducation)
	else:
		form = StudentEducationForms(request.POST or None, request.FILES or None)
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse_lazy("college:student_education"))
	context = {"form": form}
	return render(request, 'student/student_education.html', context)

class StudentEducationUpdate(LoginRequiredMixin, UpdateView):
	model = PreviousEducation
	template_name = 'student/student_education.html'
	fields = '__all__'
	success_url = reverse_lazy("college:student_education")

	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    context['update'] = True
	    return context

@login_required
def StudentCourseDetails(request):
	if not request.user.profile.previouseducation_set.all():
		return redirect(reverse_lazy("college:student_education"))
	if hasattr(request.user.profile, 'coursedetail'):
		form = StudentCourseExist(request.POST or None, instance=request.user.profile.coursedetail)
	else:
		form = StudentCourseForms(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse_lazy("college:student_course_preview"))
	context = {"form": form}
	return render(request, 'student/student_course.html', context)

@login_required
def getSubjects(request):
	course_id = request.POST.get("course")
	if course_id == '':
		raise Http404("course does not exist")
	course = get_object_or_404(Courses, pk=course_id)
	d = {}
	for i in course.subject_set.all():
		d[i.pk] = i.name
	return JsonResponse(d)


class StudentDetailsPreview(LoginRequiredMixin, TemplateView):
	models = Profile
	template_name = "student/student_course_preview.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		profile = self.request.user.profile
		st = (p.feehead.pk for p in profile.studentfee_set.all())
		context['fm'] = FeeMaster.objects.filter(course=profile.coursedetail.hons_paper.course,\
						feehead__id__in=st,
						gender=profile.gender,
						category=profile.category,
						status=1,
						board=profile.coursedetail.hons_paper.course.college.board,
			)
		if profile.studentfee_set.all() and context['fm']:
			context['fee'] = context['fm'].aggregate(Sum('amount'))['amount__sum'] + \
							sum([i.practical.amount for i in profile.coursedetail.get_Practical()]) if \
							profile.coursedetail.get_Practical() else 0
			context['practical'] = [i.name for i in profile.coursedetail.get_Practical()]
		else:
			context['fee'] = 0
		return context

import hashlib
import datetime
from pythonkit.checksum import Checksum
chk = Checksum()

@login_required
def PaymentInit(request):
	profile = request.user.profile
	st = (p.feehead.pk for p in profile.studentfee_set.all())
	if profile.studentfee_set.all():
		context = {}
		context['fm'] = FeeMaster.objects.filter(course=profile.coursedetail.hons_paper.course,\
						feehead__id__in=st,
						gender=profile.gender,
						category=profile.category,
						status=1,
						board=profile.coursedetail.hons_paper.course.college.board,
			)
		context['fee'] = "%.2f" % (context['fm'].aggregate(Sum('amount'))['amount__sum'] + \
						sum([i.practical.amount for i in profile.coursedetail.get_Practical()]) if \
						profile.coursedetail.get_Practical() else 0)
		context['practical'] = [i.name for i in profile.coursedetail.get_Practical()]
		alldata = request.user.email + request.user.first_name + request.user.last_name + str(context['fee']) + "order1"
		today = datetime.datetime.now().strftime ("%Y-%m-%d")
		context['privatekey'] = chk.encrypt('2953945' + ":|:" + '2YfVuCSV', 'rAa9fvRTuMx5gGMZ')
		context['checksum'] = chk.calculateChecksum(alldata + today, context['privatekey'])
		return render(request, 'registration/payment_init.html', context)
	else:
		raise Http404

def PaymentReceipt(request):
	return render(request, 'registration/print-order-invoice.html', {})

def PaymentConfirmation(request):
	if request.method == 'POST':
		r = Response(text=request.POST, host=request.META['HTTP_HOST'])
		r.save()
		return HttpResponse(request.POST)

def Register(request):
	if request.method == 'POST':
		try:
			user = User.objects.get(username=request.POST['username'])
			if not user.profile.status:
				return JsonResponse({'message': 'Your profile not verify, please contact'})
			if user.is_active:
				return JsonResponse({'message': 'you are already registered please login'})
			else:
				dob = request.POST['dob'].split('-')
				user.profile.dob = date(int(dob[0]), int(dob[1]), int(dob[2]))
				user.profile.save()
				dob = ''.join(dob)
				user.set_password(dob)
				user.is_active = True
				user.save()
				return JsonResponse({'status': True, 'message': '{} your are successfully registered, please login your username is {} and password {}'.format(user.get_full_name(), user.username, dob)
					})
		except Exception as e:
			return JsonResponse({'message': 'No Record Found'})
	return render(request, 'registration/register.html', {})

# class Register(FormView):
# 	model = User
# 	fields = '__all__'
# 	template_name = 'registration/register.html'

