from profiles.models import *
from django.contrib import admin

""" Modifies the look of the Test interface 
in the admin class such that one can add students
inline as well as their scores. """
class StudentTestInline(admin.TabularInline):
	model = StudentTest

class TestAdmin(admin.ModelAdmin):
	inlines = [
		StudentTestInline,
	]

class IepTargetInline(admin.TabularInline):
	model = IepIepTarget

class IepAdmin(admin.ModelAdmin):
	inlines = [
		IepTargetInline,
	]

class IbpTargetInline(admin.TabularInline):
	model = IbpIbpTarget

class IbpAdmin(admin.ModelAdmin):
	inlines = [
		IbpTargetInline,
	]

#=== Objects visible to the admin interface ===
admin.site.register(StaffMember)
admin.site.register(Year)
admin.site.register(SchoolClass)
admin.site.register(Student)
admin.site.register(IepTarget)
admin.site.register(Iep, IepAdmin)
admin.site.register(Ibp, IbpAdmin)
admin.site.register(IbpTarget)
#admin.site.register(CodeOfPractice)
admin.site.register(Test, TestAdmin)
admin.site.register(TestCategory)
admin.site.register(Referral)
admin.site.register(ReferralReason)




	
