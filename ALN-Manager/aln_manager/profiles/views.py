from django.template import Context, RequestContext, loader
from datetime import *
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from profiles.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

#for graphs 
from reportgen import *

#@login_required
def index(request):
	yearList = Year.objects.all().order_by('-startDate')
	template = loader.get_template('school_list.html')
	context = Context({
		'current_user': request.user,
		'years' : yearList,
	})
	return HttpResponse(template.render(context))

def userInbox(request):
	"""
	The start view for a user. Notifies a user if they 
	have any reports that they need to review such as IBPs or 
	IEPs and notifies if anyone has flagged their attention to 
	a given referral. Also has a list of options to navigate the 
	rest of the system.
	"""
	
	#get user's id from the request
	if not request.user.is_authenticated():
		#go to log in page
		return HttpResponseRedirect(reverse('profiles.views.log_in'))


	#Things to do
	if request.method == 'POST':
		action = request.POST['submit']
		if action == 'new_test':
			#create new test
			test = Test()
			test.name = "New Test"
			test.testCategory = TestCategory.objects.all()[0]
			test.dateOfTest = date.today()
			test.writtenBy = request.user
			test.save()
			test_id = test.id
			#redirect to page with new test
			return HttpResponseRedirect(reverse('profiles.views.viewTest', args=(test_id,)))
			
		elif action == 'new_referral':
			#create new referral
			ref = Referral()
			ref.dateOcurred = date.today()
			ref.reasonForReferral = ReferralReason.objects.all()[0]
			ref.writtenBy = request.user
			ref.save()
			ref_id = ref.id
			#redirect to page with new test
			return HttpResponseRedirect(reverse('profiles.views.viewReferral', args=(ref_id,)))
		elif action == 'create_report':
			#redirect to reports page
			
			return HttpResponseRedirect(reverse('profiles.views.annualReport'))
	# Get the IEPs that the user has written that 
	# have been written and have arrived their review
	# date (6 weeks away) and have not been reviewed
	user_unreviewed_ieps = Iep.objects.filter(writtenBy=request.user, dateWritten__lte=(date.today()-timedelta(6*7)))
	print len(user_unreviewed_ieps)


	# Same for IBPs
	user_unreviewed_ibps = Ibp.objects.filter(writtenBy=request.user, dateWritten__lte=(date.today()-timedelta(0)))	
	print len(user_unreviewed_ibps)
	
	template = loader.get_template('inbox.html')
	context = Context({
		'current_user': request.user,
		'user' : request.user,
		'ieps' : user_unreviewed_ieps,
	})
	return HttpResponse(template.render(context))

def log_in(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				#redirect to a success page.
				return HttpResponseRedirect(reverse('profiles.views.userInbox'))

	template = loader.get_template('login.html')
	context = Context({})
	return HttpResponse(template.render(context))

def log_out(request):
	logout(request)
	return HttpResponseRedirect(reverse('profiles.views.index'))

def studentList(request, class_id):
	theClass = SchoolClass.objects.get(id=class_id)
	classStudents = theClass.student_set.all().order_by('surname')
	template = loader.get_template('student_list.html')
	context = Context({
		'current_user' : request.user,
		'class' : theClass,
		'students' : classStudents,
	})
	return HttpResponse(template.render(context))


def studentProfile(request, student_id):
	#e.g. create new IEP for this student
	if request.method == 'POST':
		if request.POST['submit'] == "create_iep":
			current_student = Student.objects.get(pk=student_id)
			current_staffmember = request.user
			new_iep = Iep(student=current_student, writtenBy=current_staffmember)

			new_iep.save()
			#grab new iep id
			iep_id = new_iep.pk
			#redirect to the newly created IEP
			return HttpResponseRedirect(reverse('profiles.views.viewIep', args=(iep_id,)))

		elif request.POST['submit'] == "create_ibp":
			current_student = Student.objects.get(pk=student_id)
			new_ibp = Ibp(studentInvolved=current_student, codeOfPractice=CodeOfPractice.objects.all()[0], writtenBy=request.user)
			
			new_ibp.save()
			#grab new ibp id
			ibp_id = new_ibp.pk
			#redirect to the newly created IBP
			return HttpResponseRedirect(reverse('profiles.views.viewIbp', args=(ibp_id,)))
		elif request.POST['submit'] == "create_referral":
			current_student = Student.objects.get(pk=student_id)			
			current_staffmember = request.user
			referral_reason_default = ReferralReason.objects.all()[0]
			new_referral = Referral(writtenBy=current_staffmember, reasonForReferral=referral_reason_default)
			new_referral.save()
			#add current student to referral
			new_referral.studentsInvolved.add(current_student)	
			new_referral.save()
			
			#grab new referral id
			referral_id = new_referral.pk	
			#redirect to new referral
			return HttpResponseRedirect(reverse('profiles.views.viewReferral', args=(referral_id,)))
					
	try:
		print date.today()
		curr_student = Student.objects.get(id=student_id)
		ieps = curr_student.iep_set.all() # to show all ieps of this student
		ibps = curr_student.ibp_set.all() # to show all ibps of this student
		student_referrals = curr_student.referral_set.all()
		student_test = curr_student.studenttest_set.all()
		current_user = request.user
	except Student.DoesNotExist:
		raise Http404


	template = loader.get_template('student_profile.html')
	context = Context({
		'current_user' : request.user,
		'current_student' : curr_student,
		'ieps' : ieps,
		'ibps' : ibps,
		'referrals' : student_referrals,
		'tests' : student_test,
	})
	return HttpResponse(template.render(context))

def yearList(request, year):
	try:
		theYear = Year.objects.get(startDate__year=year)
		yearClasses = theYear.schoolclass_set.all() 
	except Year.DoesNotExist:
		raise Http404
	template = loader.get_template('year_list.html')
	context = Context({
		'current_user': request.user,
		'year' : theYear,
		'classes' : yearClasses,
	})
	return HttpResponse(template.render(context)) 

def viewIep(request, iep_id):
	try:
		theIep = Iep.objects.get(pk = iep_id)
	except Iep.DoesNotExist:
		raise Http404

	if request.method == 'POST':
		#save changes to the iep
		theIep.thingsToImprove = request.POST['things_to_improve']
		theIep.studentStrength = request.POST['student_strengths']


		#targets
		#current targets
		#keep or remove
		the_targets = list() 
		for iep_ieptarget in list(theIep.iepieptarget_set.all()):
			the_targets.append(iep_ieptarget.target)


		for target in the_targets:
			keep_or_remove = request.POST['target_'+str(target.id)]
			print keep_or_remove
			if keep_or_remove == 'delete':
				#remove the target from this iep
				for iep_ieptarget in list(theIep.iepieptarget_set.all()):
					if iep_ieptarget.target == target:
						#remove the junction object linking the target to
						#the iep
						iep_ieptarget.delete()

		#check if current targets achieved
		for iep_ieptarget in list(theIep.iepieptarget_set.all()):
			#	get achieved status from POST data
			target_id = iep_ieptarget.target.id
			is_target_achieved = request.POST['targetachieved_'+str(target_id)]
			if is_target_achieved == "true":
				iep_ieptarget.targetAchieved = True
			else:
				iep_ieptarget.targetAchieved = False

			iep_ieptarget.save()
		#adding new targets
		#loop through POST items for targets
		for item in request.POST.items():
			curr_key = item[0]
			curr_val = item[1]
				
			if 'target_' in curr_key:
				#get target id
				target_id = curr_key[7:]
				print '\"'+target_id+'\"'

				try:
					target = IepTarget.objects.get(id=target_id)	
					print "success"
				except IepTarget.DoesNotExist:
					print "Oh dear"
				
				if target not in the_targets:
					#new IepIepTarget junction object
					iep_ieptarget = IepIepTarget(target=target, iep=theIep, targetAchieved=False)
					iep_ieptarget.save()

		theIep.save()

	context = Context({
		'current_user': request.user,
		'iep': theIep,
		'iepTargets': IepTarget.objects.all(),
	})
	if not request.user.id == theIep.writtenBy.id:
		template = loader.get_template('view_iep.rtf')

		response = HttpResponse(mimetype='text/rtf')
		response['Content-Disposition'] = 'attachement; filename=iep_'+str(theIep.id)+'.rtf'
		response.write(template.render(context))
	
		return response
	else:
		template = loader.get_template('view_iep.html')
		return HttpResponse(template.render(context))


def viewIbp(request, ibp_id):
	try:
		theIbp = Ibp.objects.get(pk = ibp_id)
		codeOfPracticeList = CodeOfPractice.objects.all()
	except Ibp.DoesNotExist:
		raise Http404

	if request.method == 'POST':
		#save changes to the ibp
		theIbp.thingsToImprove = request.POST['things_to_improve']
		theIbp.studentStrength = request.POST['student_strengths']
		theIbp.codeOfPractice = CodeOfPractice.objects.get(id=request.POST['code_of_practice'])

		#targets
		#check current targets
		#keep or remove
		the_targets = list()	
		for ibp_ibptarget in list(theIbp.ibpibptarget_set.all()):
			the_targets.append(ibp_ibptarget.target)


		for target in the_targets:
			keep_or_remove = request.POST['target_'+str(target.id)]
			if keep_or_remove == 'delete':
				#remove the target from this ibp
				for ibp_ibptarget in list(theIbp.ibpibptarget_set.all()):
					if ibp_ibptarget.target == target:
						#remove the junction object linking the target to
						# the ibp
						ibp_ibptarget.delete()

		#check if current targets achieved
		for ibp_ibptarget in list(theIbp.ibpibptarget_set.all()):
			#get achieved status from POST data
			target_id = ibp_ibptarget.target.id
			is_target_achieved = request.POST['targetachieved_'+str(target_id)]
			if is_target_achieved == "true":
				ibp_ibptarget.targetAchieved = True
			else:
				ibp_ibptarget.targetAchieved = False
			
			ibp_ibptarget.save()	

		#adding new targets
		#loop through POST items for targets
		for item in request.POST.items():
			print "lol"
			curr_key = item[0]
			curr_val = item[1]

			if 'target_' in curr_key:
				#get target id
				target_id = curr_key[7:]
				print "LOL "+target_id

				try:
					target = IbpTarget.objects.get(id=target_id)
					print "success"
				except IbpTarget.DoesNotExist:
					print "Oh dear"

				if target not in the_targets:
					#new IbpIBpTarget junction object
					ibp_ibptarget = IbpIbpTarget(target=target, ibp=theIbp, targetAchieved=False)
					ibp_ibptarget.save() 

		theIbp.save()
	
	context = Context({
		'current_user': request.user,
		'codeOfPracticeList': codeOfPracticeList,
		'ibp': theIbp,
		'ibpTargets': IbpTarget.objects.all(),
	})
	if not request.user.id == theIbp.writtenBy.id:
		template = loader.get_template('view_ibp.rtf')
		
		response = HttpResponse(mimetype='text/rtf')
		response['Content-Disposition'] = 'attachement; filename=ibp_'+str(theIbp.id)+'.rtf'	
		response.write(template.render(context))

		return response

	else:
		template = loader.get_template('view_ibp.html')
		return HttpResponse(template.render(context))

def chooseStudents(request):
	#find selected student
	yearList = Year.objects.all()
	template = loader.get_template('choose_student.html')
	context = Context({
		'current_user': request.user,
		'user' : request.user,
		'years' : yearList,
	})
	return HttpResponse(template.render(context))

def viewTest(request, test_id):
	try:
		test_categories = TestCategory.objects.all()
		the_test = Test.objects.get(pk = test_id)
		students = Student.objects.all()
	except Test.DoesNotExist:
		raise Http404

	if request.method == "POST":
		#adding/removing students from test
		#check if remove students already added
		test_students = the_test.takenBy.all()
		print test_students

		the_test.name = request.POST['test_name']
		the_test.description = request.POST['description']
		the_test.testCategory = TestCategory.objects.get(name=request.POST['test_category'])
		the_test.save()

		for student in test_students:
			keep_or_remove = request.POST['student_'+str(student.id)]
			print keep_or_remove
			if keep_or_remove == 'delete':
				#remove the student from the test
				StudentTest.objects.get(test=the_test, student=student).delete()
			else:
				#keep students and change score to new score
				new_score = request.POST['studentscore_'+str(student.id)]
				student_test = StudentTest.objects.get(test=the_test, student=student)
				student_test.score = new_score
				student_test.save()

		#adding new students
		for item in request.POST.items():
			curr_key = item[0]
			curr_val = item[1]
			if 'student_' in curr_key:
				#get student id
				stu_id = curr_key[8:]
				print stu_id

				try:
					stu = Student.objects.get(id=stu_id)
				except Student.DoesNotExist:
					print "oh no"

				if stu not in test_students:
					#add_student to test
					new_stu_test = StudentTest(student=stu, test=the_test)
					new_stu_test.score = request.POST['studentscore_'+stu_id] 
					new_stu_test.save()
		

		
	context = Context({
		'current_user': request.user,
		'test': the_test,
		'categories': test_categories,
		'students': students,
	})
	#return RTF if not written by current user
	if not the_test.writtenBy.id == request.user.id:
		template = loader.get_template('view_test.rtf')
		response = HttpResponse(mimetype='text/rtf')
		response['Content-Disposition'] = 'attachment; filename=test_'+str(the_test.id)+'.rtf'
		response.write(template.render(context))

		return response
	else:
		template = loader.get_template('view_test.html')
		return HttpResponse(template.render(context))


def baseTest(request):
	"""
	Simply to test if the base view works.
	Should not be accessible during normal operation 
	of the system and should only be made available for 
	modification of the look and feel of the base view
	"""
	template = loader.get_template('base.html')
	context = Context({})
	return HttpResponse(template.render(context))

def viewReferral(request, referral_id):
	try:
		ref = Referral.objects.get(pk=referral_id)
	except Referral.DoesNotExist:
		return Http404

	if request.method == 'POST':

		ref.room = request.POST['room']
		ref.reasonForReferral = ReferralReason.objects.get(id=request.POST['reason_for_referral'])
		ref.otherReasonForReferral = request.POST['other_reason']
		
		#get date
		day = request.POST['day']
		month = request.POST['month']
		current_year = date.today().year
		print type(current_year)
		#ref.dateOccurred = date(current_year,month,day)
		print(date.today())
		ref.dateOccurred = date.today() 


		#adding/removing students from referral
		#check if remove students already added
		referral_students = ref.studentsInvolved.all() 	
		for student in referral_students:
			keep_or_remove = request.POST['student_'+str(student.id)]	
			print keep_or_remove
			if keep_or_remove == 'delete':
				#remove the student from the referral form
				ref.studentsInvolved.remove(student)	

		#adding new students				
		for item in request.POST.items():
			curr_key = item[0]
			curr_val = item[1]

			if 'student' in curr_key:
				#get student id
				stu_id = curr_key[8:]
				print stu_id
			
				try:
					stu = Student.objects.get(id=stu_id)	
				except Student.DoesNotExist:
					#Do nothing
					print "oh no"

				if stu not in referral_students:	
					#add student to referral
					ref.studentsInvolved.add(stu)
					
				#	ref.save()
				
					
		ref.save()


	if not request.user.id == ref.writtenBy.id:
		template = loader.get_template('view_referral.rtf')
		context = Context({
			'current_user': request.user,
			'referral': ref,
			'referralReasons': ReferralReason.objects.all(),
			'month' : range(1,31),
			'all_students': Student.objects.all(),
		})
		
		response = HttpResponse(mimetype='text/rtf')
		response['Content-Disposition'] = 'attachement; filename=referral_'+str(ref.id)+'.rtf'
		response.write(template.render(context))

	else:
		template = loader.get_template('view_referral.html')
		context = Context({
			'referral': ref,
			'referralReasons': ReferralReason.objects.all(),
			'month' : range(1,31),
			'all_students': Student.objects.all(),
		})

		response = HttpResponse(template.render(context))

	return response

def annualReport(request):
	"""Returns a PDF of all the statistics about this year's students.
	This includes a graph for each year that shows -
		- the distribution of reading ages
		- the distribution of spelling ages
		- the distribution of maths ages
		- number of IEP targets met vs not met
		- number of IBP targets met vs not met
	""" 
	# if request.method == 'POST' and request.POST['submit'] == "Create":
		#return the created graph
		# response = HttpResponse(mimetype='application/postscript')
		# response['Content-Disposition'] = 'attachment; filename=blah.ps'

		#grab form data
		# the_category = str(TestCategory.objects.get(name=request.POST['test_category']))
		# the_year = Year.objects.get(startDate__year=int(request.POST['school_year']))

		# graph = GraphGenerator(year=the_year, subject=the_category)
		# graph.generate_plot_data()
		# f = graph.generate_graph()

		# response.write(f.read())
		# return response 

	if request.method == 'POST' and request.POST['submit'] == "Raphael":
		print "yes"
		template = loader.get_template('view_graph.html')	
		the_category = str(TestCategory.objects.get(name=request.POST['test_category']))
		the_year = Year.objects.get(startDate__year=int(request.POST['school_year']))

		graph = GraphGenerator(year=the_year, subject=the_category)
		graph.generate_plot_data()
		context = Context({ 
			'current_user': request.user,
			'graph': graph,
		})
		return HttpResponse(template.render(context))
		
		
	else:
		template = loader.get_template('report.html')
	#just show the form to generate the thing
	year_list = Year.objects.all()	
	test_category_list = TestCategory.objects.all()
	
	context = Context({ 
		'current_user': request.user,
		'years': year_list,
		'test_category_list': test_category_list,
	})
	return HttpResponse(template.render(context))
