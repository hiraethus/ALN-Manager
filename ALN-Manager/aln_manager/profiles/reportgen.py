from profiles.models import *

#for Gnuplot.py
from numpy import *
#import Gnuplot, Gnuplot.funcutils
import os

class GraphGenerator:

	def __init__(self, year, subject):
		self.year = year
		self.subject = subject 


	def generate_plot_data(self):
		"""
		returns a dictionary of value pairs
		demonstrating how many children have 
		improved or failed to improve for a given
		year
		"""
		#check if year set and is an object or an int 
		#help from http://stackoverflow.com/questions/152580/whats-the-canonical-way-to-check-for-type-in-python 
		if isinstance(self.year, int):
			#calculate start date
			for yr in Year.objects.all():
				if self.year == yr.getCurrentYear():
					self.year = yr 

		if isinstance(self.subject, basestring):
			try:
				subject_obj = TestCategory.objects.get(name=self.subject)
				self.subject = subject_obj
			except TestCategory.DoesNotExist:
				print "No such subject"


		category_dict = {'decline': 0, 'No improvement': 0, '1-6 months': 0, '7-12 months': 0, '13-18 months': 0, '19+ months': 0 }


		students_in_year = [student for student in self.year.students if len(student.tests_taken) > 0] #only those who've taken a test
		for student in students_in_year:
			#get year's tests for this subject
			start_of_academic_year = self.year.startDate + timedelta((self.year.getCurrentYear()-7)*365)

			tests = StudentTest.objects.filter(test__dateOfTest__gte=start_of_academic_year, student=student, test__testCategory=self.subject)

			if len(tests) > 0:
				start_of_year_test_age = tests[0].score
				current_test_age = tests[len(tests)-1].score
				print "Start of year age:"+str(start_of_year_test_age)
				print "Current test age "+str(current_test_age)

				#get test age from end of least year
				delta_test_age = current_test_age - start_of_year_test_age 
				print "Delta test age "+str(delta_test_age)
				#talley into categories
				if delta_test_age < 0:
					category_dict['decline'] += 1
				elif delta_test_age == 0:
					category_dict['No improvement'] += 1
				elif delta_test_age in range(1,7):
					category_dict['1-6 months'] += 1
				elif delta_test_age in range(7,13):
					category_dict['7-12 months'] +=1
				elif delta_test_age in range(13,19):
					category_dict['13-18 months'] +=1
				else:
					category_dict['19+ months'] += 1

		self.category_talley = category_dict
		
	# def generate_graph(self):
		# """
		# Generates a GNUPlot histogram from the category_talley. If no
		# category_talley built, raises exception.
		# """
		# if self.category_talley == None:
			# raise Exception()

		#write list of plot values for histogram
		# plot = list()
		# for value in self.category_talley.values():
			# plot.append(value)

		# g = Gnuplot.Gnuplot(debug=1)
		# g.title(str(self.year)+" "+str(self.subject)+" ages")
		# g('set boxwidth 0.9 relative')
		# g('set style data histograms')
		# g('set style histogram cluster') 
		# g('set style fill solid 1.0 border lt -1')

		#create xtics labels with category_dict keys
		# g('unset xtics')
		# xtics_str = "set xtics ("
		# count = 0
		# for key in self.category_talley.keys():
			# xtics_str += '"'+str(key)+'" '+str(count)+' 0'
			# if count+1 < len(self.category_talley):
				# xtics_str += ','
			# count += 1
		
		# xtics_str += ')'
		# print xtics_str
		# g(xtics_str)

		# g('unset ytics')
		# g('set ytics 1')
		# g('set ylabel "Number of Students"')
		
		#create the graph
		# g.plot(plot)
		# g.hardcopy('profiles/static/out.ps', enhanced=1, color=1)

		#retrieve file object of the file
		# graph_file = open('profiles/static/out.ps')
		
		# return graph_file
