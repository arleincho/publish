from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout

from publishing.connect.forms import PublishingForm
from djcelery.models import IntervalSchedule
from djcelery.models import PeriodicTask
from djcelery.models import CrontabSchedule


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return render_to_response('home.html', {}, RequestContext(request))


def home(request):
    """Home view, displays login mechanism"""
    if request.user.is_authenticated():
        return redirect('done')
    return render_to_response('home.html', {}, RequestContext(request))

@login_required
def done(request):
    if request.method == 'POST':
        form = PublishingForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            interval = IntervalSchedule.objects.get(pk=int(cd['interval']))
            a = PeriodicTask(name='task-arley-publish-', task='publishing.tasks.tasks.publish', interval=interval, args=[request.user.id, post_id])
            a.save()
            return render_to_response('done.html', {
                'user': request.user,
                'form': form
            }, RequestContext(request))
    else:
        form = PublishingForm()
    return render_to_response('done.html', {'form': form}, RequestContext(request))