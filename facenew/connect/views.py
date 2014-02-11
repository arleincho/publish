
from facenew.connect.forms import PublishingForm
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
        form = PublishingForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            interval = IntervalSchedule.objects.get(pk=int(cd['interval']))
            message = Message.objects.get(pk=int(cd['message']))
            task_name = slug("{0}-{1}-{2}".format(request.user.username, interval, message.caption))
            a = PeriodicTask(name=task_name, task='facenew.tasks.tasks.publish', interval=interval, args=[facebook.user.id, message.id])
            a.save()
            return render_to_response('home.html', {
                'user': request.user,
                'facebook': facebook,
                'form': form
            }, RequestContext(request))
    else:
        form = PublishingForm()
    return render_to_response('home.html', {
        'form': form,
        'facebook': facebook,
    }, RequestContext(request))