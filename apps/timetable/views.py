# -*- coding: utf-8 -*-

# Django apps
from apps.session.models import UserProfile
from apps.timetable.models import TimeTable
from django.contrib.auth.models import User

from apps.subject.models import Lecture, ClassTime, ExamTime
# Django modules
from django.core.exceptions import *
from django.http import *
from django.contrib.auth.decorators import login_required
from utils.decorators import login_required_ajax
from django.conf import settings
from django.shortcuts import render
# For google calender
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from oauth2client.client import OAuth2WebServerFlow
import datetime
import httplib2
# Misc
import os
import json

# HELPER_FUNCTION_FOR_JSON
def time_to_int(some_time):
	hour, minute = map(int, str(some_time).split(':'))
	return hour * 60 + minute

def makelec_json(some_lec):
	pass

def dragresult_json(request):
#request.method will be POST (GET은 그냥 테스트용으로...)
    year = int(request.GET['year'])
    semester = int(request.GET['semester'])
    start_time = int(request.GET['start_block']) * 30 + 480
    end_time = int(request.GET['end_block']) * 30 + 480
    start_day = int(request.GET['start_day'])
    end_day = int(request.GET['end_day'])
    if start_time > end_time:
	    start_time, end_time = end_time, start_time
	end_time += 1
	if start_day > end_day:
	    start_day, end_day = end_day, start_day
	ClassTimeList = ClassTime.objects.all()
	IncludedLecture = []
	for each_ClTime in ClassTimeList:
		target_lecture = each_ClTime.lecture
		if target_lecture in IncludedLecture: continue
		if target_lecture.year == year and target_lecture.semester == semester:
		    if start_time <= time_to_int(each_ClTime.begin) and time_to_int(each_ClTime.end) <= end_time:
			    if start_day <= each_ClTime.day and each_ClTime.day <= end_day:
				    IncludedLecture.append(target_lecture)
	context = []
	for each_target_lecture in IncludedLecture:
	    context.append(makelec_json(each_target_lecture))
	return JsonResponse(context)


def test(request):
    context = {'pagetTitle': 'JADE 사용', 'youAreUsingJade': True}
    return render(request, 'test.jade', context)


def main(request):
    return render(request, 'timetable/index.html')


def show_table(request):
    seasons = ['봄', '여름', '가을', '겨울']
    u1 = User.objects.filter(username='ashe')[0]
    up1 = UserProfile.objects.filter(user=u1)[0]
    t1 = TimeTable.objects.filter(user=up1)[0]

    lecture_list = list(t1.lecture.all())
    table_of = u1.username
    year = t1.year
    season = seasons[t1.semester-1]
    table_id = t1.table_id
    table_name = "시간표 " + str(table_id+1)

    context = {
        "lecture_list": lecture_list,
        "table_of": table_of,
        "year": year,
        "season": season,
        "table_name": table_name,
    }
    return render(request, 'timetable/show.html', context)


@login_required_ajax
def calendar(request):
    """Exports otl timetable to google calender
    """
    user = request.user
    try:
        userprofile = UserProfile.objects.get(user=user)
    except:
        raise ValidationError('no user profile')

    email = user.email
    if email is None:
        return JsonResponse({'result': 'EMPTY'},
                            json_dumps_params={'ensure_ascii': False, 'indent': 4})


    with open(os.path.join(settings.BASE_DIR), 'keys/client_secrets.json') as f:
        data = json.load(f.read())
        client_id = data['installed']['client_id']
        client_secret = data['installed']['client_secret']
        api_key = data['api_key']

    FLOW = OAuth2WebServerFlow(
        client_id=client_id,
        client_secret=client_secret,
        scope='https://www.googleapis.com/auth/calendar',
        user_agent='')

    store = oauth2client.file.Storage(path)
    credentials = store.get()
    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(FLOW, store)

    http = credentials.authorize(httplib2.Http())
    service = discovery.build(serviceName='calender', version='v3', http=http, developerKey='blah')

    calendar_name = "[OTL]" + str(user) + "'s calendar"
    calendar = None

    if userprofile.calendar_id is not None:
        try:
            calendar = service.calendars().get(calendarId = userprofile.calendar_id).execute()
            if calendar is not None and calendar['summary'] != calendar_name:
                calendar['summary'] = calendar_name
                calendar = service.calendars().update(calendarId = calendar['id'], body = calendar).execute()
        except:
            pass

   #if calendar == None:
       # Make a new calender

   # TODO: Add calendar entry
