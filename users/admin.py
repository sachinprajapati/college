from django.contrib import admin

from .models import *


class ProfileUser(admin.ModelAdmin):
    search_fields = ['reg_no','clc_status']

admin.site.register(Profile, ProfileUser)
admin.site.register(Board)
admin.site.register(College)
admin.site.register(Courses)
admin.site.register(Subject)
admin.site.register(Session)
admin.site.register(Composition)
admin.site.register(FeeMaster)
admin.site.register(CourseDetail)
admin.site.register(PreviousEducation)
admin.site.register(StudentFee)
admin.site.register(practical)
admin.site.register(Response)
admin.site.register(BulkRecord)
admin.site.register(CLCYear)
admin.site.register(PaymentStatus)