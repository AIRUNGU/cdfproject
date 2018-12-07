from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render,redirect
from django.contrib.gis.geos import Point
from django.core.serializers import serialize
from cdf import models as cdf_models
from cdf import forms as cdf_forms
from cdf.models import Suggestions,Report,SecurityEvent,CdfProjects,Comment
from django.utils import timezone
from django.http import HttpResponse,JsonResponse
from cdf import Serializers as c_serializers
from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from collections import Counter
import simplejson
import pandas

def bufferPoints(request):
	bufferingpoints = []
	data = cdf_models.CdfProjects.objects.all()
	for p in data:
		bufferingpoints.append(tuple((p.lat,p.lon)))
	serializedpoints = list(bufferingpoints)
	# serializedpoints = serialize('geojson',serializedpoints)
	return JsonResponse(serializedpoints, safe=False)
def commentjson(request):
	relatedproject = []
	data = cdf_models.Comment.objects.all()
	p = cdf_models.Comment.objects.all().values()
	q = []
	counts = []
	latitudes = []
	longitude = []
	for w in p:
		q.append(w['post_id'])

	incidents_count = Counter(q)
	for x in incidents_count:
		counts.append(incidents_count[x])
	for r in data:
		latitudes.append(r.post.lat)

	for r in data:
		longitude.append(r.post.lon)

	for c,m,n in zip(counts,latitudes,longitude):
		relatedproject.append(tuple((m,n,c)))
	
	return JsonResponse(relatedproject, safe=False)
	
def home(request):
	return render(request,'temps/home.html')
def ContactPage(request):
	return render(request,'temps/contact.html')
def AboutPage(request):
	return render(request,'temps/about.html')
def projectsview(request):
	Otwenya = []
	NCS = []
	WS = []
	SCS = []
	SWS = []
	ES = []
	# sectors
	Education = []
	Security = []
	Health = []
	Administration = []
	Water = []
	Sports = []
	Environment = []
	projects = cdf_models.CdfProjects.objects.all()
	# Pagination

	paginator = Paginator(projects,4)
	page = request.GET.get('page')
	# End Pagination

	for m in projects:
		if m.location == 'Otwenya':
			Otwenya.append(m.amount)
		elif m.location == 'North Central Seme':
			NCS.append(m.amount)
		elif m.location == 'South Central Seme':
			SCS.append(m.amount)
		elif m.location == 'South West Seme':
			SWS.append(m.amount)
		elif m.location == 'East Seme':
			ES.append(m.amount)
		elif m.location == 'West Seme':
			WS.append(m.amount)
		else:
			print('No location')

	for s in projects:
		if s.sectors == 'education':
			Education.append(s.amount)
		elif s.sectors == 'security':
			Security.append(s.amount)
		elif s.sectors == 'health':
			Health.append(s.amount)
		elif s.sectors == 'administration':
			Administration.append(s.amount)
		elif s.sectors == 'water':
			Water.append(s.amount)
		elif s.sectors == 'sports':
			Sports.append(s.amount)
		elif s.sectors == 'enviroment':
			Environment.append(s.amount)

	# Sectors
	eamount = sum(Education)
	samount = sum(Security)
	hamount = sum(Health)
	aamount = sum(Administration)
	wamount = sum(Water)
	samount = sum(Sports)
	evamount = sum(Environment)
	# Wards
	Oamount = sum(Otwenya)
	ncsamount = sum(NCS)
	wsamount = sum(WS)
	scsamount = sum(SCS)
	swsamount = sum(SWS)
	esamount = sum(ES)
	print(esamount)
	query = request.GET.get('q')
	if query:
		projects = projects.filter(project__iexact=query) or projects.filter(sectors__iexact=query)
		paginator = Paginator(projects,4)
		page = request.GET.get('page')

	try:
		reports = paginator.page(page)
	except PageNotAnInteger:
		reports = paginator.page(1)
	except EmptyPage:
		reports = paginator.page(paginator.num_pages)
	index = reports.number - 1
	max_index = len(paginator.page_range)
	start_index = index - 5 if index >= 5 else 0
	end_index = index + 5 if index <= max_index - 5 else max_index
	page_range = paginator.page_range[start_index:end_index]
	return render(request,'temps/projects.html',
		{
			# 'saf':projects,
			'Ot':Oamount,
			'ncs':ncsamount,
			'ws':wsamount,
			'scs':scsamount,
			'sws':swsamount,
			'es':esamount,

			'edu':eamount,
			'sec':samount,
			'hea':hamount,
			'admi':aamount,
			'wtr':wamount,
			'sprt':samount,
			'env':evamount,

			'reports':reports,
			'page_range':page_range,
		})
def projectdetail(request,pk):
	proj = cdf_models.CdfProjects.objects.get(pk=pk)
	return render(request,'temps/projdetail.html',{'projd':proj})

def add_comment_to_post(request, pk):
    post = get_object_or_404(cdf_models.CdfProjects, pk=pk)
    if request.method == "POST":
        form = cdf_forms.CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('details', pk=post.pk)
    else:
        form = cdf_forms.CommentForm()
    return render(request, 'temps/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('details', pk=comment.post.pk) 

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('details', pk=comment.post.pk)

def suggestionview(request):
	form_class = cdf_forms.SuggestionForm
	if request.method == 'POST':
		form = form_class(data=request.POST)
		if form.is_valid():
			NewSuggestion = Suggestions()
			NewSuggestion.suggestion = request.POST.get('suggestion')
			NewSuggestion.body = request.POST.get('body')
			NewSuggestion.status = request.POST.get('status')
			NewSuggestion.name = request.POST.get('name')
			NewSuggestion.email = request.POST.get('email')
			NewSuggestion.created = timezone.now()
			NewSuggestion.save()
			return redirect('home')
		else:
			form = form_class
	return render(request,'temps/suggestion.html',{'sugg':form_class})

def ReportView(request):
	form_class = cdf_forms.SecurityReportForm
	if request.method == 'POST':
		form = form_class(request.POST,request.FILES)
		if form.is_valid():
			NewReport = Report()
			NewReport.description = request.POST.get('description')
			NewReport.opinion = request.POST.get('opinion')
			NewReport.image = request.FILES.get('image')
			coordinate_p = request.POST.get('coordinates').split(',')
			NewReport.geom = {
		        "type": "Point",
		        "coordinates": [float(coordinate_p[0]), float(coordinate_p[1])] 
		    }
			NewReport.created = timezone.now()
			NewReport.save() 
			return redirect('home')
		else:
			form = form_class
	return render(request,'temps/report.html',{'reports':form_class})


def ReportDisplay(request):
	incidents = cdf_models.Report.objects.all()
	paginator = Paginator(incidents,2)
	page = request.GET.get('page')
	query = request.GET.get('q')
	if query:
		incidents = incidents.filter(opinion__icontains=query)
		paginator = Paginator(incidents,2)
		page = request.GET.get('page')
	try:
		reports = paginator.page(page)
	except PageNotAnInteger:
		reports = paginator.page(1)
	except EmptyPage:
		reports = paginator.page(paginator.num_pages)
	index = reports.number - 1
	max_index = len(paginator.page_range)
	start_index = index - 5 if index >= 5 else 0
	end_index = index + 5 if index <= max_index - 5 else max_index
	page_range = paginator.page_range[start_index:end_index]
	return render(request,'temps/incidences.html',
		{
			'reports':reports,
			'page_range':page_range,
		})

def Incidence_json(request):
	data = serialize('geojson',cdf_models.Report.objects.all())
	return HttpResponse(data, content_type='json')
def Projects_json(request):
	data = serialize('geojson',cdf_models.CdfProjects.objects.all())
	return HttpResponse(data, content_type='json')

def ConstBoundary(request):
	data = serialize('geojson',cdf_models.Boundary.objects.all())
	return HttpResponse(data, content_type='json')

def EventView(request):
	form_class = cdf_forms.SecurityEventForm

	if request.method == 'POST':
		
		form = form_class(data=request.POST)
		if form.is_valid():
			form.save()
		else:
			form = form_class

	return render(request,'temps/event.html',{'events':form_class})

def EventDisplay(request):
	eventss = cdf_models.SecurityEvent.objects.all()
	return render(request,'temps/event.html',{'eventss':eventss})

def Events_json(request):
	data = serialize('geojson',cdf_models.SecurityEvent.objects.all())
	return HttpResponse(data, content_type='json')

def ActivityData(request):
	form_class = cdf_forms.SecurityEventForm
	if request.method == 'POST':
		form = form_class(data=request.POST)
		if form.is_valid():
			NewEvent = SecurityEvent()
			NewEvent.description = request.POST.get('description')
			NewEvent.title = request.POST.get('title')
			NewEvent.mdate = request.POST.get('mdate')
			NewEvent.mtime = request.POST.get('mtime')
			coordinate_p = request.POST.get('coordinates').split(',')
			NewEvent.venue = {
		        "type": "Point",
		        "coordinates": [float(coordinate_p[0]), float(coordinate_p[1])] 
		    }
			NewEvent.created = timezone.now()
			NewEvent.save() 
			return redirect('home')
		else:
			form = form_class
	return render(request,'temps/activities.html',{'form':form_class})

def ContactU(request):
	form_class = cdf_forms.ContactUsForm
	if request.method == 'POST':
		fullname = request.POST.get('fullname')
		email = request.POST.get('email')
		phonenumber = request.POST.get('phonenumber')
		body = request.POST.get('info')
		created = timezone.now()
		feedback = cdf_models.ContactUs.objects.create(fullname=fullname,
				email=email,
				phonenumber=phonenumber,
				body=body,
				created=created)
		feedback.save()
		return JsonResponse({'data':'Your Information has been received, Thank you for your contribution'})
	return JsonResponse({'data':'Fill The forms'})

# Serialization 

class ListCreateProjects(generics.ListCreateAPIView):
    queryset = CdfProjects.objects.all()
    serializer_class = c_serializers.ProjectSerializer

class ListCreateComment(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = c_serializers.CommentSerializer