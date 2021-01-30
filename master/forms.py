from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from django.core.exceptions import ValidationError
from django.db import connection

from users.models import *
from users.choices import *

import pandas as pd

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Row, Column

class DateInput(forms.DateInput):
    input_type = 'date'

class AddStudentForm(forms.ModelForm):
	first_name = forms.CharField()
	last_name = forms.CharField()
	feehead = forms.ChoiceField(choices=FeeHeads)
	course_name = forms.ModelChoiceField(queryset=Courses.objects.filter())

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
		    Row(
				Column('reg_no', css_class='form-group col-md-4 mb-0'),
		        Column('first_name', css_class='form-group col-md-4 mb-0'),
		        Column('last_name', css_class='form-group col-md-4 mb-0'),
		        css_class='form-row'
		    ),
		    Row(
				Column('phone', css_class='form-group col-md-3 mb-0'),
				Column('course_name', css_class='form-group col-md-3 mb-0'),
		        Column('feehead', css_class='form-group col-md-3 mb-0'),
		        Column('dob', css_class='form-group col-md-3 mb-0'),
		        css_class='form-row'
		    ),
		    'check_me_out',
		    Submit('submit', 'Submit', css_class='btn btn-primary')
		)

	class Meta:
		model = Profile
		fields = ('reg_no', 'phone', 'dob')
		widgets = {
            'dob': DateInput()
        }

	def clean_reg_no(self):
		data = self.cleaned_data
		if User.objects.filter(username=data['reg_no']).exists():
			raise forms.ValidationError("Student Already Exists with {}".format(data['reg_no']))
		return data['reg_no']

	def clean_caste(self):
		data = self.cleaned_data
		if data["category"] != "G":
			if not data.get["caste"]:
				raise ValidationError("Caste Certificate is required")
			else:
				return data['caste']
		return data['category']

	def save(self, commit=True):
		m = super(AddStudentForm, self).save(commit=False)
		# do custom stuff
		u = User(first_name=self.cleaned_data['first_name'], last_name=self.cleaned_data['last_name'], \
				username=self.cleaned_data['reg_no'], password=make_password(str(self.cleaned_data['dob'])), is_active=False
			)
		if commit:
			u.save()
			m.user = u
			m.status = True
			m.save()
			sf = StudentFee(feehead=self.cleaned_data['feehead'], profile=m)
			sf.save()
			cd = CourseDetail(profile=m, course=self.cleaned_data['course_name'])
			cd.save()
		return m

FORM_STATUS_CHOICES = [
    (False, 'Manual'),
    (True, 'Auto'),
]

from users.choices import MERIT_LIST_CHOICES
from college.settings import engine

from django.db import IntegrityError, transaction

# ren = {'Student Ref. No': 'reg_no', "Father's Name": 'f_name', "Mother's Name": 'm_name', "Gender": 'gender', \
# "Date Of Birth": 'dob', "Mobile No": 'phone', 'Category': 'category', 'Email ID': 'email', 'Whats App No.': 'whatsapp'}

ren = {'Registration No': 'reg_no', "Fathers Name": 'f_name', "Student Gender": 'gender', \
"Student DOB": 'dob', "MobileNo": 'phone', 'Category': 'category', 'Email': 'email', 'Whats App No.': 'whatsapp'}

def getUserPk(user):
	return User.objects.get(username=user).pk

class AddBulkStudent(forms.ModelForm):
	file = forms.FileField(widget=forms.FileInput(attrs={'accept': '.csv,.xlsx, .xls'}))
	form_verify_status = forms.ChoiceField(choices=FORM_STATUS_CHOICES)
	merit_list = forms.ChoiceField(choices=MERIT_LIST_CHOICES)
	feehead = forms.ChoiceField(choices=FeeHeads)
	course = forms.ModelChoiceField(queryset=Courses.objects.filter())

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
		    Row(
		        Column('form_verify_status', css_class='form-group col-md-4 mb-0'),
		        Column('merit_list', css_class='form-group col-md-4 mb-0'),
		        Column('feehead', css_class='form-group col-md-4 mb-0'),
		        css_class='form-row'
		    ),
		    Row(
				Column('course', css_class='form-group col-md-4 mb-0'),
				'file'
			),
		    Submit('submit', 'Submit', css_class='btn btn-primary'),
		)

	class Meta:
		model = BulkRecord
		fields = ('file',)

	def clean(self):
		data = self.cleaned_data
		print(data)
		try:
			with transaction.atomic():
				ext = data['file'].name.split('.')[-1]
				if ext == 'csv':
					df = pd.read_csv(data['file'])
				elif ext in ['xlsx', 'xls']:
					df = pd.read_excel(data['file'], engine='openpyxl')
				else:
					raise ValidationError('Not Valid File')
				if df['Registration No'].duplicated().any():
					raise ValidationError('Duplicated Record Exist in this file please remove first')
				df.rename(columns=ren, inplace=True)
				df.set_index('reg_no', inplace=True)
				user = df[['email']]
				user.index.names = ['username']
				old_user = pd.read_sql("select * from {}".format(User.objects.model._meta.db_table), engine, index_col='username')
				s1 = pd.merge(user, old_user, how='inner', on=['username'])
				if User.objects.filter(username__in=tuple(user.index.tolist())).exists():
					raise ValidationError('Dubplicate Record Exist {} Please Remove them First'.format(len(s1.index.tolist())))
				user['first_name'] = df['Student Name'].str.split().str[:-1].str.join(' ')
				user['last_name'] = df['Student Name'].str.split().str[-1]
				user['is_staff'] = False
				user['is_superuser'] = False
				user['date_joined'] = pd.Timestamp.utcnow()
				user['password'] = 'admin123'
				user['is_active'] = False
				user.to_sql(User.objects.model._meta.db_table, engine, if_exists='append')
				profile = df[['f_name', 'phone']]
				profile['status'] = data['form_verify_status']
				profile['merit'] = data['merit_list']
				alluser = pd.read_sql("select id as user_id, username from {}".format(User.objects.model._meta.db_table), engine, index_col='username')
				s2 = pd.merge(alluser, profile, how='inner', on=['username'])
				s2.index.names = ['reg_no']
				s2['clc_status'] = False
				s2.to_sql(Profile.objects.model._meta.db_table, engine, if_exists='append')
				pf = pd.read_sql("select id as profile_id, reg_no from {}".format(Profile.objects.model._meta.db_table), engine, index_col='reg_no')
				pf1 = pd.merge(pf, s2, how='inner', on=['reg_no'])
				pf1.set_index('profile_id', inplace=True)
				pf1['feehead'] = data['feehead']
				pf1['dt'] = pd.Timestamp.utcnow()
				pf1 = pf1[['feehead', 'dt']]
				pf1.to_sql(StudentFee.objects.model._meta.db_table, engine, if_exists='append')
				pf1['course_id'] = data['course'].id
				course = pf1['course_id']
				course.to_sql(CourseDetail.objects.model._meta.db_table, engine, if_exists='append')
		except Exception as e:
			raise ValidationError(e)
		return data

class AddFeeForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(AddFeeForm, self).__init__(*args, **kwargs)
		for i in CATEGORY:
			self.fields[i[1]] = forms.IntegerField()
			self.fields[i[1]].widget.attrs['class'] = 'form-control'

	class Meta:
		model = FeeMaster
		fields = '__all__'
		exclude = ('status', 'category', 'amount')

	def clean(self):
		data = self.cleaned_data
		if FeeMaster.objects.filter(course=data['course'], feehead=data['feehead'], gender=data['gender'], board=data['board']).exists():
			raise forms.ValidationError("Fee Structure already exists")
		return data


	def save(self, commit=True):
		m = super(AddFeeForm, self).save(commit=False)
		data = self.cleaned_data
		for i in CATEGORY:
			fm = FeeMaster(course=data['course'], feehead=data['feehead'], gender=data['gender'], board=data['board'], \
			category=i[0], amount=data[i[1]], status="1")
			fm.save()
		return m

class UpdateFeeForm(forms.ModelForm):
	class Meta:
		model = FeeMaster
		fields = '__all__'
		exclude = ('status', )