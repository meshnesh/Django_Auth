from datetime import timedelta, datetime, time
import math

from email.mime.text import MIMEText
import vobject

def ical(dtstart, dtend, summary, path):
	"""
	Creates an ical object; sendable in email.
	"""
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

def calc_dist(lat1, lon1, lat2, lon2):
	'''
	a function to calculate the distance in miles between two 
	points on the earth, given their latitudes and longitudes in degrees
	'''


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
	print "Didt"
	# return distance in miles
	return earth_radius * c