from django_filters import rest_framework as filters
import django_filters
import django_tables2 as tables
import itertools
from django.utils.html import format_html

from users.models import *

class PaidStudentFilter(filters.FilterSet):
	profile__reg_no = django_filters.CharFilter(lookup_expr='contains')
	amount__gt = django_filters.NumberFilter(field_name='amount', lookup_expr='gt')

	class Meta:
	    model = PaymentStatus
	    fields = ('profile__reg_no', 'profile__phone', 'easepayid', 'profile__coursedetail__course')

class PaidStudentTable(tables.Table):
	class Meta:
	    model = PaymentStatus
	    template_name = "django_tables2/bootstrap.html"
	    fields = ('profile.reg_no', 'profile.user.first_name', 'profile.f_name', 'profile.phone', \
	    		'profile.coursedetail.course', 'easepayid', 'amount', 'created_at')
	    attrs = {"class": "table table-bordered table-hover"}


class PaidCLCFilter(filters.FilterSet):
	profile__reg_no = django_filters.CharFilter(lookup_expr='contains')
	amount__gt = django_filters.NumberFilter(field_name='amount', lookup_expr='gt')

	class Meta:
	    model = PaymentStatus
	    fields = ('profile__reg_no', 'easepayid', 'profile__clcstudent__course')

class PaidCLCTable(tables.Table):
	class Meta:
	    model = PaymentStatus
	    template_name = "django_tables2/bootstrap.html"
	    fields = ('profile.reg_no', 'profile.user.first_name', 'profile.f_name', 'profile.phone', \
	    		'profile.clcstudent.course', 'easepayid', 'amount', 'created_at')
	    attrs = {"class": "table table-bordered table-hover"}


class BoardListTable(tables.Table):
	get_absolute_url = tables.Column(verbose_name='Edit')
	class Meta:
		model = Board
		fields = ('name', 'status', 'get_absolute_url')
		exclude = ('id', )
		template_name = "django_tables2/bootstrap.html"

	def render_get_absolute_url(self, value):
		print('value is', value)
		return format_html('<a href="{}"><i class="fa fa-pencil" aria-hidden="true"></i></a>', value)


class CourseListTable(tables.Table):
	get_absolute_url = tables.Column(verbose_name='Edit')
	class Meta:
		model = Courses
		fields = ('name', 'status', 'get_absolute_url')
		exclude = ('id', )
		template_name = "django_tables2/bootstrap.html"

	def render_get_absolute_url(self, value):
		print('value is', value)
		return format_html('<a href="{}"><i class="fa fa-pencil" aria-hidden="true"></i></a>', value)

class SubjectListTable(tables.Table):
	get_absolute_url = tables.Column(verbose_name='Edit')
	class Meta:
		model = Subject
		fields = ('course', 'name', 'status', 'get_absolute_url')
		exclude = ('id', )
		template_name = "django_tables2/bootstrap.html"

	def render_get_absolute_url(self, value):
		print('value is', value)
		return format_html('<a href="{}"><i class="fa fa-pencil" aria-hidden="true"></i></a>', value)

class PSubjectListTable(tables.Table):
	get_absolute_url = tables.Column(verbose_name='Edit')
	class Meta:
		model = practical
		fields = ('subject', 'amount', 'get_absolute_url')
		exclude = ('id', )
		template_name = "django_tables2/bootstrap.html"

	def render_get_absolute_url(self, value):
		return format_html('<a href="{}"><i class="fa fa-pencil" aria-hidden="true"></i></a>', value)

class SessionListTable(tables.Table):
	get_absolute_url = tables.Column(verbose_name='Edit')
	class Meta:
		model = Session
		fields = ('name', 'From', 'to', 'status', 'get_absolute_url')
		exclude = ('id', )
		template_name = "django_tables2/bootstrap.html"

	def render_get_absolute_url(self, value):
		return format_html('<a href="{}"><i class="fa fa-pencil" aria-hidden="true"></i></a>', value)

class CompositionListTable(tables.Table):
	get_absolute_url = tables.Column(verbose_name='Edit')
	class Meta:
		model = Composition
		fields = ('course', 'sub', 'get_absolute_url')
		exclude = ('id', )
		template_name = "django_tables2/bootstrap.html"

	def render_get_absolute_url(self, value):
		return format_html('<a href="{}"><i class="fa fa-pencil" aria-hidden="true"></i></a>', value)

class FeeMasterListTable(tables.Table):
	get_absolute_url = tables.Column(verbose_name='Edit')
	class Meta:
		model = FeeMaster
		fields = ('course', 'feehead', 'board', 'gender', 'category', 'status', 'get_absolute_url')
		exclude = ('id', )
		template_name = "django_tables2/bootstrap.html"

	def render_get_absolute_url(self, value):
		return format_html('<a href="{}"><i class="fa fa-pencil" aria-hidden="true"></i></a>', value)

class CLCFeeListTable(tables.Table):
	get_absolute_url = tables.Column(verbose_name='Edit')
	class Meta:
		model = CLCFee
		fields = ('course', 'fee_type', 'fee', 'get_absolute_url')
		exclude = ('id', )
		template_name = "django_tables2/bootstrap.html"

	def render_get_absolute_url(self, value):
		return format_html('<a href="{}"><i class="fa fa-pencil" aria-hidden="true"></i></a>', value)

class StudentTable(tables.Table):
	get_absolute_url = tables.Column(verbose_name='Edit')
	class Meta:
		model = Profile
		fields = ('reg_no', 'phone', 'user__email', 'get_absolute_url')

	def render_get_absolute_url(self, value):
		return format_html('<a href="{}"><i class="fa fa-pencil" aria-hidden="true"></i></a>', value)