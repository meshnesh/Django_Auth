from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from urllib import quote_plus
from django.contrib import messages



# Kiilu imports and nigger
# Rendering views

from .models import SimplePlace, Create_opportunity, RequestApplication, Dated
from .forms import SingleSkillForm, PlacedForm, SkillsForm, DateForm, addForm, ApplyForm
from datetime import timedelta, datetime, time
from django.db import transaction
from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.template import Context, Template, RequestContext
from smtplib import SMTPRecipientsRefused
import vobject
from email.mime.text import MIMEText

# Math class
import math

from django.db.models import Q


# Create your views here.
def index(request):
	context = {}
	template = 'profiles/index.html'
	return render(request, template, context)
	
def usertype(request):
	context = {}
	template = 'profiles/usertype.html'
	return render(request, template, context)

def seeker(request):
	context = {}
	template = 'profiles/seekerProfile.html'
	return render(request, template, context)
	

def helper(request):
#begin available hours	
	available = Dated.objects.filter(
		Q(user__exact=request.user.id)
		).last()
#begin committed hours
	#gets total hours for all opportunities
	commited = RequestApplication.objects.values('requests_id').filter(
		Q(user__exact=request.user.id)
		) 
	#working on hours for committed commitments
	commitments = Create_opportunity.objects.filter(
		Q(id__in=commited)
		)
	#working on hours for committed commitments
	completed = Create_opportunity.objects.filter(
		Q(id__in=commited)&
		Q(stopping_date__lt=timezone.now()) #checks whether stopping date is past (simple if statement)
		)
	print commitments
	#initiate a counter for commited and completed opportunuties
	summation, complete = 0, 0
	for com in completed:
		complete += int(com.hours_required)
	for requested in commitments:
		summation += int(requested.hours_required)


	context = {
		'available': available,
		'commited': commited,
		'sum': summation,
		'complete': complete,
	}
	template = 'profiles/helperProfile.html'
	return render(request, template, context)
	
	
def browseOpportunity(request):
	context = {}
	template = 'profiles/helperProfile.html'
	return render(request, template, context)	
	
	
# Chris Kiilu
def location(request):
	# coordinates page view
	form = PlacedForm(data = request.POST)
	nearby_places = []
	other_places = SimplePlace.objects.values('coordinates', 'location')
	
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		
		for place in other_places:
			if place['coordinates'].split(",") != ['']:
				lat = float(place['coordinates'].split(",")[0])
				lng = float(place['coordinates'].split(",")[1])
				current_lat = float(instance.coordinates.split(",")[0])
				current_lng = float(instance.coordinates.split(",")[1])
				
				# Calculate places within a certain distance
				distance = calc_dist(current_lat, current_lng, lat, lng)
		
				if distance < 50.0 and instance.location != place['location']:
					nearby_places.append(place)


		# Remove duplicates
		nearby_places = [dict(tupleized) for tupleized in set(tuple(item.items()) for item in nearby_places)]
					
		return redirect('days')

	

	context = {
		'other_places':nearby_places,	
		'form':form,
	}
	return render(request, "project/location.html", context)
	
def skills(request):
	form = SkillsForm(data = request.POST)	
	singleskill = SingleSkillForm(data=request.POST)
	query = request.GET.get("q")
	if query:
		form.fields['skills'].queryset = form.fields['skills'].queryset.filter(Q(skill__icontains=query))
		
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user =request.user
		instance.save()
		form.save_m2m()
		return redirect('helper')
	else:
		form = SkillsForm()
		
	if singleskill.is_valid():
		instance = singleskill.save(commit=False)
		instance.save()
	else:
		singleskill = SingleSkillForm()

	context = {
		"form": form,
		'singleskill': singleskill,
	}
	return render(request, "project/skills.html", context)

def days(request):
	date = DateForm(data = request.POST)
	if date.is_valid():
		instance = date.save(commit=False)
		instance.user = request.user
		instance.save()
		return redirect('skills')
	context = {
		'date': date,
	}
	return render(request, "project/days.html", context)
	
def calc_dist(lat1, lon1, lat2, lon2):
	'''a function to calculate the distance in miles between two 
	points on the earth, given their latitudes and longitudes in degrees'''


	# covert degrees to radians
	lat1 = math.radians(lat1)
	lon1 = math.radians(lon1)
	lat2 = math.radians(lat2)
	lon2 = math.radians(lon2) 

	# get the differences
	delta_lat = lat2 - lat1 
	delta_lon = lon2 - lon1 

	# Haversine formula, 
	# from http://www.movable-type.co.uk/scripts/latlong.html
	a = ((math.sin(delta_lat/2))**2) + math.cos(lat1)*math.cos(lat2)*((math.sin(delta_lon/2))**2) 
	c = 2 * math.atan2(a**0.5, (1-a)**0.5)
	# earth's radius in km
	earth_radius = 6371
	# return distance in miles
	return earth_radius * c

def current_opportunities(request):
	current = Create_opportunity.objects.filter(
		Q(user__exact=request.user.id)&
		Q(stopping_date__gt=timezone.now())&
		Q(starting_date__lte=timezone.now() + timedelta(days=30))
		)
	context = {
		'current':current,
	}
	return render(request, 'profiles/current_opportunities.html', context)
	
def single_request(request, id=None):
	opportunity = get_object_or_404(Create_opportunity, id = id)
	current_ids = RequestApplication.objects.values('user_id').filter(requests=opportunity)
	offers = User.objects.values().filter(
		Q(id__in=current_ids)
		)
	print offers
	context = {
		'opportunity':opportunity,
		'offers':offers,
	}
	return render(request, 'profiles/single_request.html', context)


def ical(dtstart, dtend, summary, path):
	cal = vobject.iCalendar()
	cal.add('method').value = 'PUBLISH'  # IE/Outlook needs this

	vevent = cal.add('vevent')
	vevent.add('dtstart').value = dtstart
	vevent.add('dtend').value = dtend
	vevent.add('summary').value = summary
	vevent.add('uid').value = path
	vevent.add('dtstamp').value = datetime.now()

	icalstream = cal.serialize()
	part = MIMEText(icalstream,'calendar')
	part.add_header('Filename','request.ics') 
	part.add_header('Content-Disposition','attachment; filename=request.ics') 
	return part

def helper_request(request, id=None):
	print request.user
	opportunity = get_object_or_404(Create_opportunity, id = id)
	if not RequestApplication.objects.filter(requests=opportunity).exists():
		form = ApplyForm(data = request.POST or None)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.requests = opportunity
			print "Obj not exist"
			instance.save()
			message_body = "This is an notification for a job involving:\n" + opportunity.description +\
				"\nThe job requires the following skills: " + ", ".join([skill['skill'] for skill in opportunity.skills.values('skill')]) 
				
			subject, from_email, to = opportunity.title, 'justinjestscurrae@gmail.com', [request.user.email]
			calendar = ical(
					opportunity.starting_date,
					opportunity.stopping_date,
					opportunity.title,
					"https://sccial-ckiilu.c9users.io/" + str(opportunity.get_absolute_url())
					)
			print (calendar)
			html_content = Template("""
			<p>This is an notification for a job involving:</p>
			<div style="margin-left:55px;">{{ opportunity.description }}</div>
			<p>The job requires the following skills:</p>
			<ul style="list-style-type:none;">
			{% for skill in opportunity.skills.all %}			
			<li>{{ skill }}</li>
	  		{% endfor %}
			</ul>
			""").render(RequestContext(request, {'opportunity': opportunity}))
			msg = EmailMultiAlternatives(subject, message_body, from_email, to)
			msg.attach_alternative(html_content, "text/html")
			try:
				msg.attach(calendar)
			except AssertionError:
				print("Whaaat! AssertionError!")
			msg.send()
		else:
			form = ApplyForm()
			print "Obj not exist, form invalid"
	else:
		form = ApplyForm(data = request.POST or None, instance=opportunity)		
		current_request = RequestApplication.objects.get(requests=opportunity).application
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			print "Obj exists"
		else:
			form = ApplyForm()
			print "Obj exists, form invalid"
		RequestApplication.objects.get(requests=opportunity).delete()
	
	print opportunity.title
	context = {
		'opportunity':opportunity,
		'form': form,
	}
	return render(request, 'profiles/browseOpportunity.html', context)
def commitments(request):
	current_ids = RequestApplication.objects.values('requests_id').filter(
		Q(user__exact=request.user.id)
		)
	current = Create_opportunity.objects.filter(id__in=current_ids)
	print current
	context = {
		'current':current,
	}
	return render(request, 'profiles/commitments.html', context)

#############################################################
#frank

#create opportunity form view
def create_opportunity_form(request):
    form = addForm(data = request.POST or None)
    if form.is_valid():
        instance = form.save(commit = False)
        instance.user = request.user
        print form.cleaned_data.get("description")
        instance.save()
        print form.cleaned_data.get("skills")
        form.save_m2m()
        
        return redirect('/seeker/')
    else:
    	print("Form invalid")
    context = {
        'form' : form
    }
    return render(request, 'profiles/create_opportunity.html', context)
    
def browse(request):	
    show_items = Create_opportunity.objects.order_by('-created_date')
    context = {
        'show_items': show_items
    }
    return render(request, 'profiles/browse.html', context)
    
def view_profile(request):
	# name = user.username
	location = SimplePlace.objects.get(user=request.user.id).location
	current = Create_opportunity.objects.filter(
		Q(user__exact=request.user.id) &
		Q(stopping_date__gt=timezone.now()) &
		Q(starting_date__lte=timezone.now() + timedelta(days=30))
	)

	context={
		# 'user':name,
		'location': location,
		'current': current,

	}
	return render(request, 'profiles/view_profile.html', context)    
   
###############################################################    