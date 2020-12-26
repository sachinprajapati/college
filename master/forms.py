from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from django.core.exceptions import ValidationError
from django.db import connection

from users.models import *
from users.choices import *

import pandas as pd

class DateInput(forms.DateInput):
    input_type = 'date'

class AddStudentForm(forms.ModelForm):
	first_name = forms.CharField()
	last_name = forms.CharField()
	course_name = forms.ChoiceField(choices=FeeHeads)

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

	def save(self, commit=True):
		m = super(AddStudentForm, self).save(commit=False)
		# do custom stuff
		u = User(first_name=self.cleaned_data['first_name'], last_name=self.cleaned_data['last_name'], \
				username=self.cleaned_data['reg_no'], password=make_password(str(self.cleaned_data['dob']))
			)
		if commit:
			u.save()
			m.user = u
			m.status = True
			m.save()
			sf = StudentFee(feehead=self.cleaned_data['course_name'], profile=m)
			sf.save()
		return m

FORM_STATUS_CHOICES = [
    (False, 'Manual'),
    (True, 'Auto'),
]

from users.choices import MERIT_LIST_CHOICES
from django.conf import settings

user = settings.DATABASES['default']['USER']
password = settings.DATABASES['default']['PASSWORD']
database_name = settings.DATABASES['default']['NAME']
host = settings.DATABASES['default']['HOST']

database_url = 'postgresql://{user}:{password}@{localhost}:5432/{database_name}'.format(
    user=user,
    password=password,
    localhost=host,
    database_name=database_name,
)

from sqlalchemy import create_engine
from django.db import IntegrityError, transaction

engine = create_engine(database_url, echo=False)

ren = {'Student Ref. No': 'reg_no', "Father's Name": 'f_name', "Mother's Name": 'm_name', "Gender": 'gender', \
"Date Of Birth": 'dob', "Mobile No": 'phone', 'Category': 'category', 'Email ID': 'email', 'Whats App No.': 'whatsapp'}

def getUserPk(user):
	return User.objects.get(username=user).pk

class AddBulkStudent(forms.ModelForm):
	file = forms.FileField(widget=forms.FileInput(attrs={'accept': '.csv,.xlsx, .xls'}))
	form_verify_status = forms.ChoiceField(choices=FORM_STATUS_CHOICES)
	merit_list = forms.ChoiceField(choices=MERIT_LIST_CHOICES)
	course = forms.ChoiceField(choices=FeeHeads)

	class Meta:
		model = BulkRecord
		fields = ('file',)

	def clean(self):
		data = self.cleaned_data
		print(data)
		try:
			with transaction.atomic():
				df = pd.read_excel(data['file'], engine='openpyxl')
				df.rename(columns=ren, inplace=True)
				df.set_index('reg_no', inplace=True)
				user = df[['email']]
				user.index.names = ['username']
				old_user = pd.read_sql("select * from {}".format(User.objects.model._meta.db_table), engine, index_col='username')
				s1 = pd.merge(user, old_user, how='inner', on=['username'])
				if User.objects.filter(username__in=tuple(user.index.tolist())).exists():
					raise ValidationError('Dubplicate Record Exist {}'.format(len(s1.index.tolist())))
				user['first_name'] = df['Student Name'].str.split().str[:-1].str.join(' ')
				user['last_name'] = df['Student Name'].str.split().str[-1]
				user['is_staff'] = False
				user['is_superuser'] = False
				user['date_joined'] = pd.Timestamp.utcnow()
				user['password'] = 'admin123'
				user['is_active'] = False
				user.to_sql(User.objects.model._meta.db_table, engine, if_exists='append')
				profile = df[['f_name', 'm_name', 'phone']]
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
				pf1['feehead'] = data['course']
				pf1['dt'] = pd.Timestamp.utcnow()
				pf1 = pf1[['feehead', 'dt']]
				pf1.to_sql(StudentFee.objects.model._meta.db_table, engine, if_exists='append')
		except Exception as e:
			raise ValidationError(e)
		return data


class AddFeeForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(AddFeeForm, self).__init__(*args, **kwargs)
		for i in CATEGORY:
			self.fields[i[1]] = forms.IntegerField()

	class Meta:
		model = FeeMaster
		fields = '__all__'
		exclude = ('status', 'category', 'amount')

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