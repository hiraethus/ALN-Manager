from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'aln_manager.views.home', name='home'),
    # url(r'^aln_manager/', include('aln_manager.foo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),

    # Application stuff
	url(r'^$', 'profiles.views.index'),
	url(r'^choose_student/$', 'profiles.views.chooseStudents'),
	url(r'^year/(?P<year>\d+)$', 'profiles.views.yearList'),	
	url(r'^class/(?P<class_id>\d+)$', 'profiles.views.studentList'),	
	url(r'^student/(?P<student_id>\d+)$', 'profiles.views.studentProfile'),
	url(r'^iep/(?P<iep_id>\d+)$', 'profiles.views.viewIep'),
	url(r'^ibp/(?P<ibp_id>\d+)$', 'profiles.views.viewIbp'),
	url(r'^test/(?P<test_id>\d+)$', 'profiles.views.viewTest'),
	url(r'^referral/(?P<referral_id>\d+)$', 'profiles.views.viewReferral'),
	url(r'^report/$', 'profiles.views.annualReport'),
	url(r'^login/$', 'profiles.views.log_in'),
	url(r'^inbox/$', 'profiles.views.userInbox'),
	url(r'^logout/$', 'profiles.views.log_out'),
)