# -*- coding: utf-8 -*-

from celery import task
from celery import Task
from celery.task import periodic_task
from facenew.tasks.models import Message
from fandjango.models import User
from facenew.whatsapp.models import Telephone
from facenew.whatsapp.models import Account
from facenew.whatsapp.models import MessagesTelephone


from djcelery.models import CrontabSchedule
from djcelery.models import PeriodicTask
from facenew.tasks.models import UserCrontabSchedule
from facenew.utils import slug

from unidecode import unidecode
from django.db import transaction

import time, datetime
from datetime import timedelta
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
    messages = Message.objects.filter(date=datetime.date.today(), crontab=cron_id, type_message='facebook', enabled=True)
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

@task(base=DBTask, rate_limit="20/m")
def message_whatsapp(account, cron_id):
    account = Account.objects.get(phone=account, enabled=True)
    password = base64.b64decode(bytes(account.password.encode('utf-8')))
    phone_number = account.phone
    messages = Message.objects.filter(date__gte=datetime.date.today(), crontab=cron_id, type_message='whatsapp', enabled=True)
    for i in range(15):
        time.sleep(4)
        for message in messages:
            phone = Telephone.objects.select_for_update(
                updated=True, exists=True, last_seen__year=datetime.datetime.now().year).exclude(
                pk__in=MessagesTelephone.objects.filter(message=message, sended=True).values_list('phone', flat=True)
            ).first()
            MessagesTelephone.objects.create(phone=phone, message=message, sended_at=datetime.datetime.now(), sended=True)
            wa = WhatsappEchoClient(phone, message.message.encode('utf-8'))
            wa.login(phone_number, password)



@task(base=DBTask, name="facenew.task.task.share_facebook")
def share_facebook(user):
    crontabs = Message.objects.filter(type_message='facebook', enabled=True).values('crontab').distinct('crontab')
    for cron in crontabs:
        interval_crontab = CrontabSchedule.objects.get(pk=int(cron['crontab']))
        task_name = slug("{0}-{1}".format(user.facebook_username, interval_crontab))
        periodic_task = PeriodicTask(name=task_name, task='facenew.tasks.tasks.publish', crontab=interval_crontab, enabled=True, args=[user.id, interval_crontab.id])
        periodic_task.save()
        user_periodic_task = UserCrontabSchedule(user=user, periodic_task=periodic_task)
        user_periodic_task.save()
    return True


@task(base=DBTask, name="facenew.task.task.cancel_facebook")
def cancel_facebook(user_id):
    PeriodicTask.objects.filter(pk__in=UserCrontabSchedule.objects.filter(user=user_id).values_list('periodic_task', flat=True)).update(enabled=False)
    return True


@task(base=DBTask, name="facenew.task.task.enabled_facebook")
def enabled_facebook(user_crontabs):
    PeriodicTask.objects.filter(pk__in=[task['periodic_task'] for task in user_crontabs]).update(enabled=True)
    return True