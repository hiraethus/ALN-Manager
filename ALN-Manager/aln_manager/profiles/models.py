from django.db import models
from django.db.models import Max
from django.forms import ModelForm

from datetime import date
from datetime import timedelta

from django.contrib.auth.models import User

class StaffMember(models.Model):
	""" The user profile for a staffmember on the system. Will also identify 
		the Staff member's permissions from the 'role' attribute. """

	user = models.OneToOneField(User) #needed to link to user account

	TITLE_ENUM = (
		(u'Mr', 	u'Mr'),
		(u'Ms', 	u'Ms'),
		(u'Mrs',	u'Mrs'),
		(u'Dr', 	u'Dr')
	)
	ROLE_ENUM = (
		(u'TE',	u'Teacher'),
		(u'HY',	u'Head of Year'),
		(u'SN', u'SEN Coordinator'),
		(u'HD', u'Headmaster')
	)
	title  = models.CharField(max_length=3, choices=TITLE_ENUM)
	role = models.CharField(max_length=2, choices=ROLE_ENUM)

	def __unicode__(self):
		full_name = self.user.get_full_name()
		return u'%s %s' % (self.title, full_name)

class Year(models.Model):
	#The year in which a student currently is in
	startDate = models.DateField(primary_key=True)
	headOfYear = models.ForeignKey(User)

	@property
	def students(self):
	#"""Get all the students in this year"""
		#return Student.objects.filter(formClass=SchoolClass.objects.get(year=self))
		classes_in_year = SchoolClass.objects.filter(year=self)
		return [student for student in Student.objects.all() \
			if student.formClass in classes_in_year]

	def getCurrentYear(self):
	# calculates the year (e.g. year 7, 8, 9, 10)
	# NOTE: only works for comprehensive schools	
		timePast = (date.today() - self.startDate)
		daysPast = timePast.days
		currentYear = (daysPast / 365) + 7
		return currentYear

	def __unicode__(self):
		return u'Year %d' % (self.getCurrentYear())

	def getStartDateString(self):
	# Returns string of date in the format YYYY-MM-DD
		return u'%s' % (self.startDate.isoformat())

class SchoolClass(models.Model):
	year = models.ForeignKey(Year)
	formTutor = models.ForeignKey(User)	
	name = models.CharField(max_length=15)

	def __unicode__(self):
		return u'%s, %s' % (self.name, self.year)

class Student(models.Model):
	GENDER_ENUM = (
		(u'M', u'Male'),
		(u'F', u'Female')
	)
	LEFTHANDED_ENUM = (
		(u'T', u'Yes'),
		(u'F', u'No')
	)
	forename = models.CharField(max_length=25)
	surname = models.CharField(max_length=25)
	gender = models.CharField(max_length=2, choices=GENDER_ENUM)
	dateOfBirth = models.DateField() 
	formClass = models.ForeignKey(SchoolClass)
	isLeftHanded = models.CharField(max_length=1, choices=LEFTHANDED_ENUM)
	backgroundInfo = models.TextField()
	
	@property
	def tests_taken(self):
		return StudentTest.objects.filter(student=self)

	#following will help with generating annual reports
	def current_test_age(self, test_category):
		try:
			#get latest test taken by student
			self.tests_taken
			spelling_tests_taken_by_student = Test.objects.filter(takenBy=tests_taken_by_student, testCategory = test_category)
			latest_spelling_test = spelling_tests_taken_by_student.latest('dateOfTest')
			
			current_spelling_age = StudentTest.objects.get(test=latest_spelling_test, student=self).score
		except Exception:
			#Student hasn't yet taken a test
			current_spelling_age = -1 

		return int(current_spelling_age)

	@property
	def current_spelling_age(self):
		return int(self.current_test_age("spelling"))

	@property
	def current_mathematics_age(self):
		return self.current_test_age("mathematics")

	def __unicode__(self):
		return u'%s %s' % (self.forename, self.surname)


class IepTarget(models.Model):
	target = models.CharField(max_length=100)

	def __unicode__(self):
		return u'%s' % (self.target)


class Iep(models.Model):
	"""Individual Education Plan"""
	writtenBy = models.ForeignKey(User)
	student = models.ForeignKey(Student)
	dateWritten = models.DateField(auto_now_add=True)
	thingsToImprove = models.TextField()
	studentStrength = models.TextField()
	targets = models.ManyToManyField(IepTarget, through='IepIepTarget')
	
	@property
	def review_date(self):
		"""Returns the date at which this IBP must be 
				reviewed."""
		timeUntilReview = timedelta(6*7)
		reviewDate = self.dateWritten+timeUntilReview

		return reviewDate

	def __unicode__(self):
		return u'%s, %s' % (self.dateWritten, self.student)


class IepIepTarget(models.Model):
	"""Junction table for an IEP's targets such that
	we can have a targetAchieved field for checking the progress of 
	targets achieved"""
	target = models.ForeignKey(IepTarget)
	iep = models.ForeignKey(Iep)
	targetAchieved = models.BooleanField()

class IbpTarget(models.Model):
	target = models.CharField(max_length=100)

	def __unicode__(self):
		return u'%s' % (self.target)

class CodeOfPractice(models.Model):
	name = models.CharField(max_length=60)
	description = models.TextField()

	def __unicode__(self):
		return u'%s' % (self.name)

class Ibp(models.Model):
	writtenBy = models.ForeignKey(User)
	studentInvolved = models.ForeignKey(Student)
	dateWritten = models.DateField(auto_now_add=True)
	thingsToImprove = models.TextField()
	studentStrengths = models.TextField()
	codeOfPractice = models.ForeignKey(CodeOfPractice, blank=True)
	targets = models.ManyToManyField(IbpTarget, through='IbpIbpTarget')
	
	@property
	def review_date(self):
		"""Returns the date at which this IBP must be 
				reviewed."""
		timeUntilReview = timedelta(6*7)
		reviewDate = dateWritten+timeUntilReview

		return reviewDate

	def __unicode__(self):
		return u'%s, %s' % (self.dateWritten, self.studentInvolved)

class IbpIbpTarget(models.Model):
	"""Junction table between IBP and an IBP Target allowing a number of targets
	To be listed and also allows indicating of target achievement with 'targetAchieved'
	field"""
	target = models.ForeignKey(IbpTarget)
	ibp = models.ForeignKey(Ibp)
	targetAchieved = models.BooleanField()
	

class TestCategory(models.Model):
	"""The kind of test. This could be the subject (e.g. 
		Maths, French etc.) or a particular kind of skills 
		test."""
	name = models.CharField(max_length = 60, primary_key=True)
	description = models.TextField(blank=True)

	def __unicode__(self):
		return (u'%s') % (self.name)

class Test(models.Model):
	name = models.CharField(max_length=60)
	testCategory = models.ForeignKey(TestCategory)
	description = models.TextField()
	dateOfTest = models.DateField()
	takenBy = models.ManyToManyField(Student, through='StudentTest')
	writtenBy = models.ForeignKey(User, blank=True)

	def __unicode__(self):
		return (u'%s') % (self.name)

class StudentTest(models.Model):
	"""Junction Table linking a student to a test
		and providing the student's score for the test"""
	student = models.ForeignKey(Student)
	test = models.ForeignKey(Test)
	score = models.PositiveIntegerField()

class ReferralReason(models.Model):
	description = models.CharField(max_length = 200)
	
	def __unicode__(self):
		return (u'%s') % (self.description)

class Referral(models.Model):
	dateOcurred = models.DateField(auto_now_add=True)
	room = models.CharField(max_length=60)
	studentsInvolved = models.ManyToManyField(Student)
	reasonForReferral = models.ForeignKey(ReferralReason)
	otherReasonForReferral = models.TextField()
	writtenBy = models.ForeignKey(User, blank=True)

	def __unicode__(self):
		return u'%s %s' % (self.dateOccurred, self.writtenBy.get_full_name())
