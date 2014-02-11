
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.conf import settings
from fandjango.decorators import facebook_authorization_required

@facebook_authorization_required()
def home(request):
    """Home view, displays login mechanism"""
    return render_to_response('home.html', {}, RequestContext(request))

