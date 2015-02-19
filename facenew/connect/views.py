# -*- coding: utf-8 -*-

# from facenew.connect.forms import SelectOptionForm
# from facenew.connect.forms import TIME_INTERVALS
from facenew.tasks.models import Message
# from djcelery.models import IntervalSchedule
from djcelery.models import PeriodicTask
from djcelery.models import CrontabSchedule
from facenew.tasks.models import UserCrontabSchedule
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from fandjango.decorators import facebook_authorization_required
from facenew.tasks.tasks import cancel_facebook
from facenew.tasks.tasks import share_facebook
from facenew.tasks.tasks import enabled_facebook


@csrf_exempt
@facebook_authorization_required()
def done(request):
    if request.facebook.user:
        facebook = request.facebook
        user_crontabs = UserCrontabSchedule.objects.filter(user_id=facebook.user.id).values('periodic_task')

        donacion = facebook.user.donate

        if request.method == 'POST':
            if request.POST.get('donate', False):
                facebook.user.donate = True
                facebook.user.save()

        if donacion:
            if len(user_crontabs) > 0:
                enabled_facebook.delay(user_crontabs)
            else:
                share_facebook.delay(facebook.user)
        else:
            return render_to_response('index.html', {}, RequestContext(request))
            

        return render_to_response('done.html', {'donacion': donacion}, RequestContext(request))
        # else:
            # if len(user_crontabs) > 0:
            #     enabled_facebook.delay(user_crontabs)
            #     return render_to_response('done.html', {}, RequestContext(request))



@csrf_exempt
@facebook_authorization_required()
def cancel(request):
    if request.facebook.user:
        facebook = request.facebook
        if request.method == 'POST':
            cancel_facebook.delay(facebook.user)
    return render_to_response('index.html', {}, RequestContext(request))
