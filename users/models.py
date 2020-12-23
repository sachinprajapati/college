from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from datetime import date

from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.urls import reverse_lazy

from .choices import *
import os

class OverwriteStorage(FileSystemStorage):

	def get_available_name(self, name, max_length):
		if self.exists(name):
		    os.remove(os.path.join(settings.MEDIA_ROOT, name))
		return name

def student_directory(instance, filename):
    ext = filename.split('.')[-1]
    return 'student/{0}/photo.{1}'.format(instance.user.id, ext)

def sign_directory(instance, filename):
    ext = filename.split('.')[-1]
    return 'student/{0}/sign.{1}'.format(instance.user.id, ext)

def clc_directory(instance, filename):
    ext = filename.split('.')[-1]
    return 'student/{0}/clc.{1}'.format(instance.user.id, ext)

def caste_directory(instance, filename):
    ext = filename.split('.')[-1]
    return 'student/{0}/caste.{1}'.format(instance.user.id, ext)

def migration_directory(instance, filename):
    ext = filename.split('.')[-1]
    return 'student/{0}/migration.{1}'.format(instance.user.id, ext)

def cota_directory(instance, filename):
    ext = filename.split('.')[-1]
    return 'student/{0}/cota.{1}'.format(instance.user.id, ext)

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	reg_no = models.CharField(max_length=255, unique=True)
	f_name = models.CharField(max_length=255, verbose_name="Father Name", null=True)
	m_name = models.CharField(max_length=255, verbose_name="Mother Name", null=True)
	gender = models.CharField(max_length=1, choices=GENDER, null=True)
	dob = models.DateField(null=True)
	m_status = models.CharField(max_length=1, choices=MARITAL_STATUS, null=True)
	adhar_regex = RegexValidator(regex=r'^(\+\d{1,3})?,?\s?\d{16}', message="Adhar number must be 16 digits long.")
	adhar = models.PositiveIntegerField(validators=[adhar_regex], null=True, blank=True)
	phone_regex = RegexValidator(regex=r'^(\+\d{1,3})?,?\s?\d{10}', message="Phone number must be entered in the format: '+999999999'. Up to 10 digits allowed.")
	phone = models.DecimalField(validators=[phone_regex], max_digits=10, decimal_places=0)
	whatsapp = models.DecimalField(validators=[phone_regex], max_digits=10, decimal_places=0, null=True)
	address = models.TextField(null=True)
	state = models.PositiveSmallIntegerField(choices=STATE, null=True)
	city = models.CharField(max_length=255, null=True)
	district = models.CharField(max_length=255, null=True)
	pin_regex = RegexValidator(regex=r'^(\+\d{1,3})?,?\s?\d{6}', message="Pincode number must be 6 digits long.")
	pincode = models.PositiveIntegerField(validators=[pin_regex], null=True)
	religion = models.CharField(max_length=1, choices=RELIGION_LIST, null=True)
	category = models.CharField(max_length=1, choices=CATEGORY, null=True)
	g_occupation = models.CharField(max_length=255, verbose_name="Gurdian Occupation", null=True)
	g_income = models.PositiveIntegerField(verbose_name="Gurdian Annual Income", null=True)
	phy_disabled = models.CharField(max_length=1, choices=DISABLED, null=True)
	img = models.ImageField(upload_to=student_directory, verbose_name="Student Passport Photo", null=True, storage=OverwriteStorage())
	sign = models.ImageField(upload_to=sign_directory, verbose_name="Student Signature", null=True, storage=OverwriteStorage())
	clc = models.ImageField(upload_to=clc_directory, null=True, blank=True, storage=OverwriteStorage())
	caste = models.ImageField(upload_to=caste_directory, null=True, blank=True, verbose_name="Caste-EWS", storage=OverwriteStorage())
	migration = models.ImageField(upload_to=migration_directory, null=True, blank=True, verbose_name="Migration Certificate", storage=OverwriteStorage())
	cota = models.ImageField(upload_to=cota_directory, null=True, blank=True, verbose_name="SPECIAL COTA DOCUMENT", storage=OverwriteStorage())
	status = models.BooleanField(default=False)
	merit = models.PositiveIntegerField(choices=MERIT_LIST_CHOICES, null=True)


class Board(models.Model):
	name = models.CharField(max_length=255, verbose_name="Board Name", unique=True)
	status = models.CharField(max_length=1, choices=BOOLEAN_STATUS)

	def __str__(self):
		return '{}'.format(self.name)

	def get_absolute_url(self):
		return reverse_lazy('master:update_board', args=[str(self.id)])

def college_directory(instance, filename):
    return 'college_{0}/{1}'.format(instance.id, filename)


class College(models.Model):
	name = models.CharField(max_length=255, verbose_name="College Name", unique=True)
	address = models.TextField()
	city = models.CharField(max_length=255)
	district = models.CharField(max_length=255)
	pin_code = models.PositiveIntegerField()
	board = models.ForeignKey(Board, on_delete=models.CASCADE)
	logo = models.ImageField(upload_to=college_directory, storage=OverwriteStorage())

	def __str__(self):
		return '{}'.format(self.name)

	def get_absolute_url(self):
		return 


class Courses(models.Model):
	name = models.CharField(max_length=255, verbose_name="Course Name", unique=True)
	status = models.CharField(max_length=1, choices=BOOLEAN_STATUS)
	college = models.ForeignKey(College, on_delete=models.CASCADE)

	def __str__(self):
		return '{}'.format(self.name)

	def get_absolute_url(self):
		return reverse_lazy('master:update_course', args=[str(self.id)])


class Subject(models.Model):
	course = models.ForeignKey(Courses, on_delete=models.CASCADE)
	name = models.CharField(max_length=255, verbose_name="Subject Name", unique=True)
	status = models.CharField(max_length=1, choices=BOOLEAN_STATUS)
	is_practical = models.BooleanField(null=True)

	def __str__(self):
		return '{}'.format(self.name)

	def get_absolute_url(self):
		return reverse_lazy('master:update_subject', args=[str(self.id)])


class Session(models.Model):
	name = models.CharField(max_length=9, verbose_name="Session Name", unique=True)
	From = models.DateField()
	to = models.DateField()
	status = models.CharField(max_length=1, choices=BOOLEAN_STATUS)

	def __str__(self):
		return '{}'.format(self.name)

	def get_absolute_url(self):
		return reverse_lazy('master:update_session', args=[str(self.id)])


class Composition(models.Model): #Optional Subject
	course = models.ForeignKey(Courses, on_delete=models.CASCADE, verbose_name="Course Name")
	sub = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Subject Name")

	def __str__(self):
		return 'course {} sub {}'.format(self.course, self.sub)

	def get_absolute_url(self):
		return reverse_lazy('master:update_composition', args=[str(self.id)])

	class Meta:
	    constraints = [
	        models.UniqueConstraint(fields=['course', 'sub'], name='Subject already exist in with this course')
	    ]

class FeeMaster(models.Model):
	course = models.ForeignKey(Courses, on_delete=models.CASCADE)
	feehead = models.PositiveIntegerField(choices=FeeHeads)
	gender = models.CharField(max_length=1, choices=GENDER)
	category = models.CharField(max_length=1, choices=CATEGORY)
	status = models.CharField(max_length=1, choices=BOOLEAN_STATUS)
	board = models.ForeignKey(Board, on_delete=models.CASCADE)
	amount = models.PositiveIntegerField()


PASSOUT_YEAR = [(year%100, year) for year in range(date.today().year, 1984, -1)]

def student_marksheet(instance, filename):
    ext = filename.split('.')[-1]
    return 'student/{0}/marksheet.{1}'.format(instance.profile.user.id, ext)

class PreviousEducation(models.Model):
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
	course = models.CharField(max_length=255, choices=PREVIOUS_COURSE, verbose_name="Course Name")
	stream = models.CharField(max_length=1, choices=STREAM)
	passout = models.PositiveIntegerField(choices=PASSOUT_YEAR)
	board = models.ForeignKey(Board, on_delete=models.CASCADE)
	scholl_name = models.CharField(max_length=255)
	marks_type = models.PositiveSmallIntegerField(choices=MARKS_TYPE)
	total_marks = models.PositiveSmallIntegerField()
	obtained_marks = models.PositiveSmallIntegerField()
	marksheet = models.ImageField(upload_to=student_marksheet, storage=OverwriteStorage())

	def get_marks_perc(self):
		return (self.obtained_marks*100)/self.total_marks

ACADEMIC_SESSION = [(str(year)+"-"+str(year+1), str(year)+"-"+str(year+1)) for year in range(date.today().year, 1984, -1)]

class CourseDetail(models.Model):
	profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
	course = models.ForeignKey(Courses, on_delete=models.CASCADE)
	last_session = models.CharField(max_length=9, choices=ACADEMIC_SESSION)
	enroll_session = models.ForeignKey(Session, on_delete=models.CASCADE)
	inter_marks = models.PositiveIntegerField(verbose_name='12th Marksheet No', null=True)
	inter_roll_code = models.PositiveIntegerField(null=True, blank=True, verbose_name="12'th Roll Code")
	inter_roll_no = models.PositiveIntegerField(verbose_name="12'th Roll No", null=True)
	hons_paper = models.ForeignKey(Subject, on_delete=models.CASCADE)
	sub1_paper = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="sub1_paper", null=True)
	sub2_paper = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="sub2_paper", null=True)
	comp_paper = models.ForeignKey(Composition, on_delete=models.CASCADE, null=True)

	def get_Practical(self):
		return [i for i in (self.hons_paper, self.sub1_paper, self.sub2_paper) if i.is_practical and hasattr(i, 'practical')]


class StudentFee(models.Model):
	feehead = models.PositiveIntegerField(choices=FeeHeads)
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
	dt = models.DateTimeField(auto_now_add=True)

class practical(models.Model):
	subject = models.OneToOneField(Subject, on_delete=models.CASCADE)
	amount = models.PositiveIntegerField()


class Response(models.Model):
	text = models.TextField()
	host = models.CharField(max_length=255)

def excel_file(instance, filename):
    return 'master/files/{}'.format(filename)

class BulkRecord(models.Model):
	file = models.FileField(upload_to=excel_file)
	dt = models.DateTimeField(auto_now_add=True)