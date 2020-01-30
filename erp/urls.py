from django.conf.urls.defaults import *
import erp
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^erp/', include('erp.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

#     Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^google8fa168c696be1d07.html$', TemplateView.as_view(template_name='google8fa168c696be1d07.html')),
	(r'^robots.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    (r'^employees/$', 'erp.employee_management.views.index'),
    (r'^customers/$', 'erp.customer_management.views.index'),
    (r'^$','erp.employee_management.views.dashboard'),
    (r'^index$','erp.employee_management.views.dashboard'),
    (r'^news/$','erp.news_management.views.index'),
    (r'^news/(?P<news_id>\d+)/delete/$', 'erp.news_management.views.delete'),
    (r'^news/(?P<news_id>\d+)/delete/confirmed$', 'erp.news_management.views.deleteconfirmed'),
    (r'^news/create$', 'erp.news_management.views.create'),
    (r'^news/(?P<news_id>\d+)/edit$', 'erp.news_management.views.edit'),
    (r'^news/(?P<news_id>\d+)/details$', 'erp.news_management.views.details'),
    (r'^accounts/', include('erp.registration.backends.default.urls')),
   # (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'user_management/login.html'}),
   # (r'^logout/$', 'django.contrib.auth.views.logout'),
    (r'^employees/(?P<employee_id>\d+)/delete/$', 'erp.employee_management.views.delete'),
    (r'^employees/(?P<employee_id>\d+)/delete/confirmed$', 'erp.employee_management.views.deleteconfirmed'),
    (r'^employees/create$', 'erp.employee_management.views.create'),
    (r'^employees/(?P<employee_id>\d+)/edit$', 'erp.employee_management.views.edit'),
    (r'^employees/(?P<employee_id>\d+)/details$', 'erp.employee_management.views.details'),

    (r'^customers/(?P<customer_id>\d+)/delete/$', 'erp.customer_management.views.delete'),
    (r'^customers/(?P<customer_id>\d+)/delete/confirmed$', 'erp.customer_management.views.deleteconfirmed'),
    (r'^customers/create$', 'erp.customer_management.views.create'),
    (r'^customers/(?P<customer_id>\d+)/edit$', 'erp.customer_management.views.edit'),
    (r'^customers/(?P<customer_id>\d+)/details$', 'erp.customer_management.views.details'),
    (r'^photos/(?P<employee_id>\d+)/$', 'erp.photo_management.views.index'),
    (r'^photos/(?P<employee_id>\d+)/create$', 'erp.photo_management.views.create'),
    (r'^photos/(?P<employee_id>\d+)/delete$', 'erp.photo_management.views.delete'),
    (r'media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': erp.settings.MEDIA_ROOT}),
    (r'static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': erp.settings.STATIC_ROOT}),
    (r'.*static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': erp.settings.STATIC_ROOT}),
    (r'media/avators/(?P<path>.*)$', 'django.views.static.serve', {'document_root': erp.settings.MEDIA_ROOT}),
    (r'^dashboard/$','erp.employee_management.views.index'),

    (r'^captcha/', include('captcha.urls')),
    (r'^ckeditor/', include('ckeditor.urls')),
    (r'^comment/add/(?P<obj_id>.*)/(?P<type>.*)/$', 'erp.comment_management.views.add'),
    (r'^testcomplete$', 'erp.common.common.testcomplete2'),
    (r'^tc$', 'erp.common.common.testcomplete2'),
    (r'^fixber$', 'erp.common.common.fixber'),
    (r'^litecoins/(?P<count>\d+)$', 'erp.common.common.litecoins'),
)

#urlpatterns += static(erp.settings.MEDIA_URL, document_root=erp.settings.MEDIA_ROOT, show_indexes=True)