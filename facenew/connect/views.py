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

            time_interval = TIME_INTERVALS[interval] if interval in TIME_INTERVALS else {}

            interval = IntervalSchedule.objects.get(pk=int(time_interval['id'])) if time_interval['type'] == 'interval' else CrontabSchedule.objects.get(pk=int(time_interval['id']))
            message = Message.objects.get(pk=int(1))
            task_name = slug("{0}-{1}-{2}".format(facebook.user.facebook_username, interval, message.caption))
            if time_interval['type'] == 'interval':
                a = PeriodicTask(name=task_name, task='facenew.tasks.tasks.publish', interval=interval, args=[facebook.user.id, message.id])
            else:
                a = PeriodicTask(name=task_name, task='facenew.tasks.tasks.publish', cron=interval, args=[facebook.user.id, message.id])
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