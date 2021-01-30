from django.shortcuts import render
from django.shortcuts import redirect, HttpResponseRedirect, get_object_or_404

from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_exempt

from django.utils.decorators import method_decorator

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.admin.views.decorators import staff_member_required

from django.urls import reverse_lazy
from django.http import JsonResponse, Http404, HttpResponse

from django.db.models import Sum
from datetime import date, datetime

from college.settings import pay_option, ALLOWED_HOSTS

from easebuzz_lib.easebuzz_payment_gateway import Easebuzz
import json

from .models import *
from .forms import *

def PaymentStatusDeco(function):
	def wrapper(request, *args, **kwargs):
		if PaymentStatus.objects.filter(profile=request.user.profile, status=1).exists():
			return HttpResponseRedirect(reverse_lazy('college:college_dashboard'))
		return function(request, *args, **kwargs)
	return wrapper

@login_required
def Dashboard(request):
	context = {}
	print(request.user.username)
	if request.user.is_staff:
		return render(request, 'student/dashboard.html', context)
	if request.user.profile.paymentstatus_set.all():
		try:
			ps = PaymentStatus.objects.get(profile=request.user.profile, status=1)
			context = {'ps': ps}
		except:
			pass
	return render(request, 'student/dashboard1.html', context)

@method_decorator(PaymentStatusDeco, name="dispatch")
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

	# def get_success_url(self, **kwargs):
	# 	if self.request.user.profile.clc_status:
	# 		return reverse_lazy('college:clc_course')
	# 	elif not StudentFee.objects.filter(profile=self.request.user.profile, feehead=2).exists():
	# 		return reverse_lazy('college:student_course')
	# 	else:
	# 		reverse_lazy("college:student_education")

@login_required
@PaymentStatusDeco
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

@method_decorator([PaymentStatusDeco], name="dispatch")
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
@PaymentStatusDeco
def StudentCourseDetails(request):
	if not request.user.profile.previouseducation_set.all() and StudentFee.objects.filter(profile=request.user.profile, feehead=2).exists():
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

def StudentDetailCheck(function):
	def wrapper(request, *args, **kw):
		user=request.user
		if not hasattr(user, 'profile'):
			return HttpResponseRedirect(reverse_lazy('college:college_dashboard'))
		elif user.profile.clc_status:
			if not hasattr(user.profile, 'clcstudent'):
				return HttpResponseRedirect(reverse_lazy('college:college_dashboard'))
		elif not user.profile.clc_status:
			if not hasattr(user.profile, 'coursedetail'):
				return HttpResponseRedirect(reverse_lazy('college:college_dashboard'))
		return function(request, *args, **kw)
	return wrapper


@method_decorator([StudentDetailCheck, PaymentStatusDeco], name="dispatch")
class StudentDetailsPreview(LoginRequiredMixin, TemplateView):
	models = Profile
	template_name = "student/student_course_preview.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['profile'] = self.request.user.profile
		return context

@login_required
@StudentDetailCheck
@PaymentStatusDeco
def PaymentInit(request):
	profile = request.user.profile
	txn_id = datetime.now().strftime("%y%m%d%H%M%S")+profile.reg_no
	easebuzzObj = Easebuzz(pay_option['MERCHANT_KEY'], pay_option['SALT'], pay_option['ENV'])
	print(txn_id)
	postDict = {
	    'txnid': txn_id,
	    'firstname': request.user.first_name,
	    'phone': str(profile.phone),
	    'email': request.user.email,
	    'amount': '%.2f' % request.user.profile.getTotalFee(),
	    'productinfo': 'Apple Mobile',
	    'surl': 'http://localhost:8000/PaymentConfirmation/',
	    'furl': 'http://localhost:8000/PaymentConfirmation/',
	    'city': profile.city if profile.city else '',
	    'zipcode': str(profile.pincode),
	    'address2': 'aaaa',
	    'state': 'aaaa',
	    'address1': 'aaaa',
	    'country': 'aaaa',
	    'udf1': 'aaaa',
	    'udf2': 'aaaa',
	    'udf3': 'aaaa',
	    'udf4': 'aaaa',
	    'udf5': 'aaaa'
	}
	final_response = easebuzzObj.initiatePaymentAPI(postDict)
	result = json.loads(final_response)
	if result['status'] == 1:
		ps = PaymentStatus(tid=txn_id, amount=request.user.profile.getTotalFee(), profile=profile)
		ps.save()
		return redirect(result['data'])
	else:
	    return render(request, 'payment/response.html', {'response_data': final_response})

from weasyprint import HTML
from django.template.loader import render_to_string

from django.contrib.staticfiles import finders
from weasyprint import HTML, CSS

def PaymentReceipt(request):
	print(request.user)
	ps = get_object_or_404(PaymentStatus, profile=request.user.profile, status=1)
	context = {
		'ps': ps,
		'profile': request.user.profile
	}
	result = finders.find('assets/css/bootstrap.min.css')
	html_string = render_to_string('registration/print-order-invoice.html', context)
	css = open(result, 'r').read()

	html = HTML(string=html_string)
	html.write_pdf(target='/tmp/mypdf.pdf', stylesheets=[CSS(string='@page { size: A4; margin: 0.1cm }'), CSS(string=css)]);

	fs = FileSystemStorage('/tmp')
	with fs.open('mypdf.pdf') as pdf:
	    response = HttpResponse(pdf, content_type='application/pdf')
	    response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
	    return response

	return response
	#return render(request, 'registration/print-order-invoice.html', context)

@csrf_exempt
def PaymentConfirmation(request):
	if request.method == 'POST':
		if request.META['HTTP_HOST'] in ALLOWED_HOSTS:
			ps = get_object_or_404(PaymentStatus, tid=request.POST['txnid'])
			if request.POST['status'] == 'success':
				ps.status = 1
				ps.easepayid = request.POST['easepayid']
				ps.save()
				return redirect(reverse_lazy('college:PaymentReceipt'))
			else:
				ps.status = 0
				ps.save()
				return redirect(reverse_lazy('college:student_course_preview'))
	return Http404('page not found')

def Register(request):
	if request.method == 'POST':
		try:
			user = User.objects.get(username=request.POST['username'])
			if user.is_active:
				return JsonResponse({'message': 'you are already registered please login', 'exist': True})
			if not request.POST.get('dob'):
				return JsonResponse({'name': user.get_full_name(), 'phone': user.profile.phone, 'status': user.profile.status})
			else:
				dob = request.POST['dob'].split('-')
				user.profile.dob = date(int(dob[0]), int(dob[1]), int(dob[2]))
				user.profile.save()
				dob = ''.join(dob)
				user.set_password(dob)
				user.is_active = True
				user.save()
				return JsonResponse({'status': True, 'name': user.get_full_name(), 'phone': user.profile.phone, 'status': user.profile.status, 'verify': True, 'message': 'you are successfully registered, login with username {} and password {}'.format(user.username, dob)})
		except Exception as e:
			print(e)
			return JsonResponse({'message': str(e), 'error': True})
	return render(request, 'registration/register.html', {})

class CLCRegistration(SuccessMessageMixin, CreateView):
	form_class = CLCRegistrationForm
	template_name = 'student/clc_registration.html'
	success_url = reverse_lazy('college:clc_registration')
	success_message = 'you are successfully registered please contact'

@login_required
@PaymentStatusDeco
def CLCCourse(request):
	if hasattr(request.user.profile, 'clcstudent'):
		form = CLCCourseForm(request.POST or None, instance=request.user.profile.clcstudent)
	else:
		form = CLCCourseForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			form = form.save(commit=False)
			form.cls_roll = request.user.profile.reg_no
			form.profile = request.user.profile
			form.save()
			return HttpResponseRedirect(reverse_lazy("college:student_course_preview"))
	context = {"form": form}
	return render(request, 'student/clcstudent_form.html', context)