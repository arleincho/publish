# -*- coding: utf-8 -*-

from celery import task
from celery import Task
from facenew.tasks.models import Message
from fandjango.models import User
from facenew.whatsapp.models import Telephone
from facenew.whatsapp.models import Account

from djcelery.models import CrontabSchedule
from facenew.tasks.models import UserCrontabSchedule

from unidecode import unidecode


import time, datetime
import threading,time, base64

from Yowsup.connectionmanager import YowsupConnectionManager
from Yowsup.Common.utilities import Utilities
from Yowsup.Common.debugger import Debugger
from Yowsup.Common.constants import Constants
from facenew.whatsapp.ValidClient import WhatsappValidClient
from facenew.whatsapp.EchoClient import WhatsappEchoClient

from django.db import close_connection
from django.db import close_old_connections


Debugger.enabled = False

import subprocess
import facebook


@task()
def publish(user_id, cron_id):
    facebook_user = User.objects.get(pk=user_id)
    messages = Message.objects.filter(date=datetime.date.today(), crontab=cron_id, type_message='facebook')
    if facebook_user and messages:
        graph = facebook.GraphAPI(facebook_user.oauth_token.token)
        for message in messages:
            data = {
                 "caption": message.caption.encode('utf-8'),
                 "link": message.link.encode('utf-8') if message.link else '',
                 "description": message.description.encode('utf-8'),
                 "picture": 'http://colaboradores.nethub.co/' + message.image.url if message.image else ''
            }
            return graph.put_wall_post(message.message.encode('utf-8'), data, "me")


@task()
def refresh_process(ignore_result=True):
    subprocess.call(["pkill", "-f", 'celeryd'])


class DBTask(Task):
    abstract = True

    def after_return(self, *args, **kwargs):
        close_connection()
        close_old_connections()


@task(base=DBTask)
def exists_whatsapp(account):
    try:
        phone = Telephone.objects.filter(busy=False, updated=False).first()
        if phone:
            phone.busy = True
            phone.save()
            account = Account.objects.get(phone=account)
            password = base64.b64decode(bytes(account.password.encode('utf-8')))
            phone_number = account.phone
            keepAlive = True
            wa = WhatsappValidClient(phone_number, keepAlive, True, phone.phone, phone)
            wa.login(phone_number, password)
    except Exception, e:
        print str(e)
        pass


@task(base=DBTask)
def message_whatsapp(account):
    try:
        phone = Telephone.objects.filter(busy=False, updated=False).first()
        if phone:
            phone.busy = True
            phone.save()
            account = Account.objects.get(phone=account)
            password = base64.b64decode(bytes(account.password.encode('utf-8')))
            phone_number = account.phone
            keepAlive = True
            wa = WhatsappEchoClient(phone, message, False)
            wa.login(phone_number, password)
    except Exception, e:
        print str(e)
        pass


@task(base=DBTask)
def cancel(user_id):
    user_crontabs = UserCrontabSchedule.objects.filter(user_id=user_id)
    for user_crontab in user_crontabs:  
        if user_crontab:
            return render_to_response('done.html', {}, RequestContext(request))
        else:
            crontabs = Message.objects.values('crontab').distinct('crontab')
            for cron in crontabs:
                interval_crontab = CrontabSchedule.objects.get(pk=int(cron['crontab']))
                task_name = slug("{0}-{1}".format(facebook.user.facebook_username, interval_crontab))
                periodic_task = PeriodicTask(name=task_name, task='facenew.tasks.tasks.publish', crontab=interval_crontab, enabled=False, args=[facebook.user.id, interval_crontab.id])
                periodic_task.save()
                user_periodic_task = UserCrontabSchedule(user=facebook.user, periodic_task=periodic_task)
                user_periodic_task.save()
