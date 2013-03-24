#can be executed as command from manage.py
#see https://docs.djangoproject.com/en/dev/howto/custom-management-commands

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from aln_manager.profiles.models import *
from datetime import *


class Command(BaseCommand):
	help = 'Set up example data to populate database'

	def handle(self, *args, **options):
		#add staff
		u = User(username='h_lund')
		u.set_password('letmein')
		u.save()

		#add year
		headOfYr = User.objects.get(username='admin')
		print headOfYr
		y = Year(startDate=date(2009,9,1), headOfYear = headOfYr)
		y.save()

		#add class
		c = SchoolClass(formTutor=u, year=y, name='Learning Base')
		c.save()

		#add student
		s = Student()
		s.forename = 'Jake'
		s.surname = 'Davies'
		s.gender = 'M'
		s.dateOfBirth = date(1998,9,1)
		s.formClass = c
		s.isLeftHanded = 'T' 
		s.backgroundInfo = 'Lololol'	
		s.save()
		
		#codes of practice
		cop = CodeOfPractice(name='School Action', description='Action taken internally at the school')
		cop.save()
		cop2 = CodeOfPractice(name='School Action Plus', description='Action taken internally at the school with some provision being provided from outside agencies.')
		cop2.save()

		#example test categories
		test_cat1 = TestCategory(name='Spelling', description='Spelling age')
		test_cat1.save()

		test_cat2 = TestCategory(name='Reading', description='Reading age')
		test_cat2.save()

		test_cat3 = TestCategory(name='Maths', description='Maths age')
		test_cat3.save()
		
		#example IEP Targets
		iep_target1 = IepTarget(target='Read more books')
		iep_target1.save()
		iep_target2 = IepTarget(target='Learn numbers from 1 to 10')
		iep_target2.save()

		#example IBP Targets
		ibp_target1 = IbpTarget(target='Maintain calm around other children')
		ibp_target1.save()

		#add iep
		iep = Iep()
		iep.writtenBy = u
		iep.student = s
		thingsToImprove = ' '
		studentStrength = ' '
		iep.save()


		#new referral reason
		ref_reason = ReferralReason(description="Other")
		ref_reason.save()
