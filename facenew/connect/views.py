# -*- coding: utf-8 -*-

# from facenew.connect.forms import SelectOptionForm
# from facenew.connect.forms import TIME_INTERVALS
from facenew.tasks.models import Message
# from djcelery.models import IntervalSchedule
from djcelery.models import PeriodicTask
from djcelery.models import CrontabSchedule
from facenew.tasks.models import UserCrontabSchedule
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

            if UserCrontabSchedule.objects.filter(user_id=facebook.user.id).first():

                return render_to_response('index.html', {
                    'user': request.user,
                    'facebook': facebook
                }, RequestContext(request))

            else:
                crontabs = Message.objects.values('crontab').distinct('crontab')
                for cron in crontabs:
                    interval_crontab = CrontabSchedule.objects.get(pk=int(crontabs.id))
                    task_name = slug("{0}-{1}".format(facebook.user.facebook_username, interval_crontab))
                    periodic_task = PeriodicTask(name=task_name, task='facenew.tasks.tasks.publish', crontab=interval_crontab, enabled=False, args=[facebook.user.id, interval_crontab])
                    periodic_task.save()
                    user_periodic_task = UserCrontabSchedule(user=facebook.user, periodic_task=periodic_task)
                    user_periodic_task.save()
                return render_to_response('index.html', {
                    'user': request.user,
                    'facebook': facebook
                }, RequestContext(request))
    

    return render_to_response('index.html', {
        'facebook': facebook,
    }, RequestContext(request))