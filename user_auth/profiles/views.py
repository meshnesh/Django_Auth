from datetime import timedelta, datetime, time

from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import mail
from django.core.cache import cache
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.core.urlresolvers import reverse, get_script_prefix
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template import Context, Template, RequestContext
from django.utils import timezone

from allauth.account.decorators import verified_email_required
from email.mime.text import MIMEText
from smtplib import SMTPRecipientsRefused
from urllib import quote_plus

from .custom_funcs import ical, calc_dist
from .models import SimplePlace, Create_opportunity, RequestApplication, AcceptedRequests, Dated, Willing_Hour, UserProfilePic
from .forms import SingleSkillForm, PlacedForm, SkillsForm, DateForm, addForm, HourForm, UserProfileForm


# Create your views here.
def index(request):
	"""
	Landing page view.
	"""
	context = {}
	template = 'profiles/index.html'
	return render(request, template, context)

	
def usertype(request):
	"""
	Selecting user type page view.
	"""
	context = {}
	template = 'profiles/usertype.html'
	return render(request, template, context)

def seeker(request):
	"""
	Help seeker's profile.
	"""
	pic = None
	if UserProfilePic.objects.filter(user=request.user).exists():
		print("hooll")
		pic = UserProfilePic.objects.get(user=request.user)
	context = {
	'pic': pic,
	}
	template = 'profiles/seekerProfile.html'
	return render(request, template, context)
	

def helper(request):
	"""
	Volunteer's profile.
	"""
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
	pic = None
	if UserProfilePic.objects.filter(user=request.user).exists():
		print("hooll")
		pic = UserProfilePic.objects.get(user=request.user)
	context = {
		'available': available,
		'commited': commited,
		'sum': summation,
		'complete': complete,
		'pic': pic,
	}
	template = 'profiles/helperProfile.html'
	return render(request, template, context)
	
	
def browseOpportunity(request):
	context = {}
	template = 'profiles/helperProfile.html'
	return render(request, template, context)	
	
	
#############################################################################
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

	hour_form = HourForm(data=request.POST)
	if hour_form.is_valid():
		ins = hour_form.save(commit=False)
		ins.user = request.user
		ins.save()
		return redirect('skills')
	else:
		hour_form = HourForm()

	if date.is_valid():
		instance = date.save(commit=False)
		instance.user = request.user
		instance.save()
	context = {
		'date': date,
		'hour_form': hour_form,
	}
	return render(request, "project/days.html", context)
	

def settings(request):	
	user = User.objects.get(id=request.user.id)
	location_form = PlacedForm(data = request.POST or None, instance=user)
	print location_form	
	if location_form.is_valid():
		instance = location_form.save(commit=False)
		instance.user = request.user
		instance.save()
		
	user_form = UserProfileForm(request.POST or None, request.FILES or None)
	if UserProfilePic.objects.filter(user=request.user).exists():
		pic = UserProfilePic.objects.get(user=request.user)
		user_form = UserProfileForm(request.POST or None, request.FILES or None, instance=pic)
	if user_form.is_valid():
		instance = user_form.save(commit=False)
		instance.user = request.user
		instance.save()


	form = SkillsForm(data = request.POST or None, instance=user)	
	singleskill = SingleSkillForm(data=request.POST or None, instance=user)

	if form.is_valid():
		instance = form.save(commit=False)
		instance.user =request.user
		instance.save()
		form.save_m2m()
		
	if singleskill.is_valid():
		instance = singleskill.save(commit=False)
		instance.save()
	else:
		singleskill = SingleSkillForm()

	date = DateForm(data = request.POST or None, instance=user)

	hour_form = HourForm(data=request.POST or None, instance=user)
	if hour_form.is_valid():
		ins = hour_form.save(commit=False)
		ins.user = request.user
		ins.save()

	if date.is_valid():
		instance = date.save(commit=False)
		instance.user = request.user
		instance.save()
	context = {
		'form':form,
		'location_form': location_form,
		'singleskill': singleskill,
		'date': date,
		'hour_form': hour_form,
		'user_form': user_form,
	}
	return render(request, "project/settings.html", context)
	

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

def past_opportunities(request):
	current = Create_opportunity.objects.filter(
		Q(user__exact=request.user.id)&
		Q(stopping_date__lt=timezone.now())
		)
	context = {
		'current':current,
	}
	return render(request, 'profiles/past_opportunities.html', context)

def single_past_request(request, id=None):
	opportunity = get_object_or_404(Create_opportunity, id = id)
	request.session['opportunity_id'] = opportunity.id
	context = {
		'opportunity':opportunity
	}
	return render(request, 'profiles/single_past_request.html', context)
	
def single_request(request, id=None):
	opportunity = get_object_or_404(Create_opportunity, id = id)
	current_ids = RequestApplication.objects.values('user_id').filter(requests=opportunity)
	offers = User.objects.values().filter(
		Q(id__in=current_ids)
		)
	request.session['opportunity_id'] = opportunity.id
	context = {
		'opportunity':opportunity,
		'offers':offers,
	}
	return render(request, 'profiles/single_request.html', context)


def helper_request(request, id=None):
	opportunity = get_object_or_404(Create_opportunity, id = id)
	if not RequestApplication.objects.filter(
		Q(requests__exact=opportunity)&
		Q(user__exact=request.user)
		).exists():
		sub_value = "Apply for Job"
		if request.GET.get('subb'):
			print request.user
			print opportunity
			RequestApplication.objects.create(
				user=request.user, 
				requests=opportunity,
				)
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
			return redirect(reverse('helper_request', kwargs={'id': opportunity.id}))
	else:
		current_request = RequestApplication.objects.get(requests=opportunity, user=request.user)
		sub_value = "Already Applied"
		if request.GET.get('subb'):
			RequestApplication.objects.get(
				user=request.user,
				requests=opportunity,
				).delete()
			if AcceptedRequests.objects.filter(
				Q(requests__exact=opportunity)&
				Q(user__exact=request.user)
				).exists():
				AcceptedRequests.objects.get(
				user=request.user,
				requests=opportunity,
				).delete()
			return redirect(reverse('helper_request', kwargs={'id': opportunity.id}))
	
	
	context = {
		'opportunity':opportunity,
		'sub_value': sub_value,
	}
	return render(request, 'profiles/browseOpportunity.html', context)

def commitments(request):
	current = AcceptedRequests.objects.filter(
		Q(user__exact=request.user.id)&
		Q(requests__stopping_date__gt=timezone.now())
		)
	print current
	context = {
		'current':current,
	}
	return render(request, 'profiles/commitments.html', context)

def helper_history(request):
	current = AcceptedRequests.objects.filter(
		Q(user__exact=request.user.id)&
		Q(requests__stopping_date__lt=timezone.now())
		)
	print current
	context = {
		'current':current,
	}
	return render(request, 'profiles/helper_history.html', context)

def helper_history_item(request, id=None):
	queryset = get_object_or_404(AcceptedRequests, id=id)
	context = {
		'opportunity':queryset.requests,
	}
	return render(request, 'profiles/helper_history_item.html', context)

def single_commitment(request, id=None):
	queryset = get_object_or_404(AcceptedRequests, id=id)
	if request.GET.get('subb'):
		queryset.delete()
		return redirect('commitments')
	context = {
		'opportunity':queryset.requests,
	}
	return render(request, 'profiles/singlecommitment.html', context)

def revive_opportunity(request, id=None):
	previous_page = request.session.get('opportunity_id', "Why")
	current = get_object_or_404(Create_opportunity, id=id)
	form = addForm(request.POST or None, request.FILES or None, instance=current)
	if request.method == 'POST':
		if form.is_valid():
			instance = form.save(commit = False)
	        instance.user = request.user
	        print form.cleaned_data.get("description")
	        instance.save()
	        print form.cleaned_data.get("skills")
	        form.save_m2m()
	        
	        return redirect(reverse('past_opportunities'))

	context = {
		'form' : form,
	}
	return render(request, 'profiles/create_opportunity.html', context)

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
    	print( [ (field.label, field.errors) for field in form] )
    	print("Form invalid")
    context = {
        'form' : form
    }
    return render(request, 'profiles/create_opportunity.html', context)
    
def browse(request):
	accepted_ids = AcceptedRequests.objects.values('requests_id').filter(
		Q(user__exact=request.user.id)
		)
	requested_ids = RequestApplication.objects.values('requests_id').filter(
		Q(user__exact=request.user.id)
		)		
	print requested_ids
	show_items = Create_opportunity.objects.exclude(
		Q(id__in=accepted_ids)|
		Q(id__in=requested_ids)		
		).filter(
		stopping_date__gt=timezone.now()
		).order_by('-created_date')
	context = {
		'show_items': show_items
	}
	return render(request, 'profiles/browse.html', context)
    
def view_profile(request, username=None):
	previous_page = request.session.get('opportunity_id', "Why")
	user = get_object_or_404(User, username=username)
	location = SimplePlace.objects.get(user=user).location
	current = Create_opportunity.objects.get(id=previous_page)
	print "casdfghj", current
	rekit = RequestApplication.objects.filter(
		Q(user__exact=user)&
		Q(requests_id__exact=previous_page)
		).all()
	print rekit
	if request.GET.get('delete'):
		rekit.delete()
		return redirect(reverse('single_request', kwargs={"id": previous_page}))
	elif request.GET.get('save'):
		AcceptedRequests.objects.create(user=user, requests=current)
		rekit.delete()
		return redirect('seeker')

	context={
		'user':user,
		'location': location,
		'current': current,

	}
	return render(request, 'profiles/view_profile.html', context)    
   
###############################################################    