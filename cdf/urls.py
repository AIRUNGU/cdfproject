
from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from cdf import views as cdf_views 
from django.views.generic import TemplateView
from djgeojson.views import GeoJSONLayerView

from cdf import models as c_models
urlpatterns = [
	path('', cdf_views.home,name='home'),
    path('about/',cdf_views.AboutPage,name='about'),
    path('contact/',cdf_views.ContactPage,name='contact'),
	path('projects/', cdf_views.projectsview,name='projects'),
    url(r'^projectsdata.geojson$', GeoJSONLayerView.as_view(model=c_models.CdfProjects, properties=('project','location','descrition','sectors','amount','status','remarks','county_nam')), name='projectsdata'),
	path(r'^report/',cdf_views.ReportView,name='report'),
	path(r'details/<int:pk>/',cdf_views.projectdetail, name = "details"),
    path('suggest/',cdf_views.suggestionview,name='suggest'),
    url(r'^incidents.geojson$', GeoJSONLayerView.as_view(model=c_models.Report, properties=('title','description','mdate','mtime')), name='incidents'),
    path(r'^incidents/',cdf_views.ReportDisplay,name='incidents'),
    path(r'incidentdata/',cdf_views.Incidence_json,name='incidentdata'),
    # path(r'projectsdata/',cdf_views.Projects_json,name='projectsdata'),
    path(r'boundary/',cdf_views.ConstBoundary,name='boundary'),
    path(r'^event/',cdf_views.EventDisplay,name='event'),
    path(r'^comj/',cdf_views.commentjson,name='comj'),
    path(r'^buffer/',cdf_views.bufferPoints,name='buffer'),
    path(r'eventsdata/',cdf_views.Events_json,name='eventsdata'),
    path(r'^activity/$',cdf_views.ActivityData, name='activity'),
    path(r'^post/(?P<pk>\d+)/comment/', cdf_views.add_comment_to_post, name='add_comment_to_post'),
    path(r'^comment/(?P<pk>\d+)/approve/', cdf_views.comment_approve, name='comment_approve'),
    path(r'^comment/(?P<pk>\d+)/remove/', cdf_views.comment_remove, name='comment_remove'),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)