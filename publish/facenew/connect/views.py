# -*- coding: utf-8 -*-

from facenew.connect.forms import SelectOptionForm
from facenew.connect.forms import TIME_INTERVALS
from facenew.tasks.models import Message
from djcelery.models import IntervalSchedule
from djcelery.models import PeriodicTask
from djcelery.models import CrontabSchedule
from facenew.utils import slug
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from fandjango.decorators import facebook_authorization_required


@csrf_exempt
@facebook_authorization_required()
def done(request):
    if request.facebook.user:
        facebook = request.facebook
    if request.method == 'POST':
        form = SelectOptionForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            time_interval = TIME_INTERVALS[cd['interval']] if cd['interval'] in TIME_INTERVALS else {}
            interval = IntervalSchedule.objects.get(pk=int(time_interval['id'])) if time_interval['type'] == 'interval' else CrontabSchedule.objects.get(pk=int(time_interval['id']))
            message = Message.objects.get(pk=int(1))
            task_name = slug("{0}-{1}-{2}-{3}".format(facebook.user.facebook_username, interval, cd['interval'], message.caption))
            interval_interval = None
            interval_crontab = None
            if time_interval['type'] == 'interval':
                interval_interval = interval
            else:
                interval_crontab = interval
            a = PeriodicTask(name=task_name, task='facenew.tasks.tasks.publish', interval=interval_interval, crontab=interval_crontab, enabled=False, args=[facebook.user.id, message.id, time_interval])
            a.save()
            return render_to_response('index.html', {
                'user': request.user,
                'facebook': facebook,
                'form': form
            }, RequestContext(request))
    else:
        form = SelectOptionForm()
    return render_to_response('index.html', {
        'form': form,
        'facebook': facebook,
    }, RequestContext(request))