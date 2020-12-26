from django import forms

from django.core.exceptions import ValidationError

from django.contrib.auth.models import User

from .models import *

class DateInput(forms.DateInput):
    input_type = 'date'

class StudentForms(forms.ModelForm):
	email = forms.EmailField()

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user')
		super(StudentForms, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
		    visible.field.widget.attrs['class'] = 'form-control'
		self.fields['address'].widget.attrs['rows'] = 4
		self.fields['img'].widget.attrs['onchange'] = "document.getElementById('id_img_display').src = window.URL.createObjectURL(this.files[0])"
		self.fields['sign'].widget.attrs['onchange'] = "document.getElementById('id_sign_display').src = window.URL.createObjectURL(this.files[0])"
		self.fields['clc'].widget.attrs['onchange'] = "document.getElementById('id_clc_display').src = window.URL.createObjectURL(this.files[0])"
		self.fields['caste'].widget.attrs['onchange'] = "document.getElementById('id_caste_display').src = window.URL.createObjectURL(this.files[0])"
		self.fields['migration'].widget.attrs['onchange'] = "document.getElementById('id_mig_display').src = window.URL.createObjectURL(this.files[0])"
		self.fields['cota'].widget.attrs['onchange'] = "document.getElementById('id_cota_display').src = window.URL.createObjectURL(this.files[0])"

	class Meta:
		model = Profile
		exclude = ('reg_no', 'dob', 'phone', 'clc_status')
		widgets = {
            'dob': DateInput()
        }

	def clean_email(self):
		data = self.cleaned_data
		if not data.get('email'):
			data['email'] = User.objects.get(pk=self.clean_user.id).email
		return data['email']

	def save(self, commit=True):
		m = super(StudentForms, self).save(commit=False)
		# do custom stuff
		if not m.user.email:
			m.user.email = self.cleaned_data['email']
			m.user.save()
		if commit:
			m.save()
		return m


class StudentEducationForms(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(StudentEducationForms, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
		    visible.field.widget.attrs['class'] = 'form-control'
		self.fields['marksheet'].widget.attrs['onchange'] = "document.getElementById('id_marksheet_display').src = window.URL.createObjectURL(this.files[0])"

	class Meta:
		model = PreviousEducation
		fields = '__all__'


class StudentCourseForms(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(StudentCourseForms, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
		    visible.field.widget.attrs['class'] = 'form-control'

	class Meta:
		model = CourseDetail
		fields = '__all__'

	def clean(self):
		data = self.cleaned_data
		if data['hons_paper'].pk == data['sub1_paper'].pk or data['hons_paper'].pk == data["sub2_paper"].pk or \
			data["sub1_paper"].pk == data["sub2_paper"].pk:
			raise forms.ValidationError("Honours Paper, Paper 1 and Paper 2 must be different subject")
		return data


class StudentCourseExist(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(StudentCourseExist, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
		    visible.field.widget.attrs['class'] = 'form-control'
		self.fields['course'].widget.attrs['readonly'] = True
		self.fields['last_session'].widget.attrs['readonly'] = True
		self.fields['enroll_session'].widget.attrs['readonly'] = True
		self.fields['hons_paper'].widget.attrs['readonly'] = True

	class Meta:
		model = CourseDetail
		# exclude = ('course', 'last_session', 'enroll_session', 'hons_paper')
		fields = '__all__'

	def clean(self):
		data = self.cleaned_data
		if data['hons_paper'].pk == data['sub1_paper'].pk or data['hons_paper'].pk == data["sub2_paper"].pk or \
			data["sub1_paper"].pk == data["sub2_paper"].pk:
			raise forms.ValidationError("Honours Paper, Paper 1 and Paper 2 must be different subject")
		return data


class SearchStudent(forms.Form):
	username = forms.CharField()

class PsubjectForm(forms.ModelForm):
	subject = forms.ModelChoiceField(queryset = Subject.objects.filter(is_practical=True) )
	class Meta:
		model = practical
		fields = '__all__'


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, Row, Column, Field

class CLCRegistrationForm(forms.ModelForm):
	# academic_session = forms.ModelChoiceField(queryset=CLCYear.objects.all())
	first_name = forms.CharField()
	last_name = forms.CharField()
	board_roll_no = forms.IntegerField()
	course = forms.ModelChoiceField(queryset=Courses.objects.all())

	class Meta:
		model = Profile
		fields = ('phone', 'dob')
		widgets = {
            'dob': DateInput()
        }

	def save(self, commit=True):
		m = super(CLCRegistrationForm, self).save(commit=False)
		data = self.cleaned_data
		m.reg_no = data['board_roll_no']
		pwd = ''.join(str(data['dob']).split('-'))
		u = User(username=data['board_roll_no'], first_name=data['first_name'], last_name=data['last_name'], \
			)
		u.set_password(pwd)
		u.save()
		m.user = u
		m.clc_status = True
		if commit:
			m.save()
		return m


class CLCCourseForm(forms.ModelForm):
	class Meta:
		model = CLCStudent
		exclude = ('profile', 'cls_roll')