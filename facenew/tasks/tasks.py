# -*- coding: utf-8 -*-

from celery import task
from celery import Task
from celery import current_app
from celery.task import periodic_task
from facenew.tasks.models import Message
from fandjango.models import User
from facenew.whatsapp.models import Telephone
from facenew.whatsapp.models import Account
from facenew.whatsapp.models import MessagesPhoneWhatsapp


from djcelery.models import CrontabSchedule
from djcelery.models import PeriodicTask
from facenew.tasks.models import UserCrontabSchedule
from facenew.utils import slug
from django.conf import settings

from unidecode import unidecode
from django.db import transaction

import time, datetime
from datetime import timedelta
import threading,time, base64
import sched
import urllib2

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
    message = Message.objects.filter(date=datetime.date.today(), crontab=cron_id, type_message='facebook', enabled=True).first()
    # if facebook_user and messages:
    graph = facebook.GraphAPI(facebook_user.oauth_token.token)
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

    # def after_return(self, *args, **kwargs):
        # close_connection()
        # close_old_connections()


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

@task(base=DBTask, ignore_result=True)
@transaction.commit_manually
def message_whatsapp(account, cron_id):

    account = Account.objects.get(phone=account, enabled=True)
    password = account.password
    phone_number = account.phone
    message = Message.objects.filter(date__lte=datetime.date.today(), crontab=cron_id, type_message='whatsapp', enabled=True).first()
    try:
        phone = Telephone.objects.select_for_update(
            exists=True, updated=True, last_seen__year=datetime.datetime.now().year).exclude(
            pk__in=MessagesPhoneWhatsapp.objects.filter(message=message, sended=True).values_list('phone', flat=True)
        ).first()
        message_phone_whatsapp = MessagesPhoneWhatsapp.objects.create(phone=phone, message=message, sended=True)
        transaction.commit()
        # wa = WhatsappEchoClient(phone.phone, message.message.encode('utf-8'))
        # wa = WhatsappEchoClient('573102436410', message.message.encode('utf-8'), False, message_phone_whatsapp)
        # wa.login(account['phone_number'], account['password'])
        image = settings.ROOT_PATH  + urllib2.unquote(message.image.url)
        script = settings.ROOT_PATH + "/whatsapp/lib/whatsapp/send.php"

        print "/usr/bin/php5 {0} {1} '{2}' {3} {4} '{5}' {6} '{7}'".format(
            script, phone_number, '', password, phone.phone, message.message.encode('utf-8'), message_phone_whatsapp.id, image)

        subprocess.call(["/usr/bin/php5 {0} {1} '{2}' {3} {4} '{5}' {6} '{7}'".format(
            script, phone_number, '', password, phone.phone, message.message.encode('utf-8'), message_phone_whatsapp.id, image)
        ], shell=True)
    except Exception, e:
        transaction.rollback()
        print str(e)


@task(ignore_result=True)
def stop_messege_whatsapp(task_id):
    PeriodicTask.objects.filter(pk__in=task_id).update(enabled=False)



# @task(ignore_result=True)
# def launch_messege_whatsapp(account, cron_id):
#     interval = 10
#     limit = 60
#     step = (limit/interval)
#     account = Account.objects.get(phone=account, enabled=True)
#     password = account.password
#     phone_number = account.phone
#     message = Message.objects.filter(date__lte=datetime.date.today(), crontab=cron_id, type_message='whatsapp', enabled=True).first()
#     if message and account:
#         s = sched.scheduler(time.time, time.sleep)
#         s.enter(3, 1,  current_app.send_task, ('facenew.tasks.tasks.message_whatsapp', ({'phone_number': phone_number, 'password': password}, message)))
#         s.enter(6, 1, current_app.send_task, ('facenew.tasks.tasks.message_whatsapp', ({'phone_number': phone_number, 'password': password}, message)))
#         s.enter(9, 1, current_app.send_task, ('facenew.tasks.tasks.message_whatsapp', ({'phone_number': phone_number, 'password': password}, message)))
#         s.enter(12, 1, current_app.send_task, ('facenew.tasks.tasks.message_whatsapp', ({'phone_number': phone_number, 'password': password}, message)))
#         s.enter(15, 1, current_app.send_task, ('facenew.tasks.tasks.message_whatsapp', ({'phone_number': phone_number, 'password': password}, message)))
#         # s.enter(18, 1, current_app.send_task, ('facenew.tasks.tasks.message_whatsapp', ({'phone_number': phone_number, 'password': password}, message)))
#         # s.enter(21, 1, current_app.send_task, ('facenew.tasks.tasks.message_whatsapp', ({'phone_number': phone_number, 'password': password}, message)))
#         # s.enter(24, 1, current_app.send_task, ('facenew.tasks.tasks.message_whatsapp', ({'phone_number': phone_number, 'password': password}, message)))
#         # s.enter(27, 1, current_app.send_task, ('facenew.tasks.tasks.message_whatsapp', ({'phone_number': phone_number, 'password': password}, message)))
#         # s.enter(30, 1, current_app.send_task, ('facenew.tasks.tasks.message_whatsapp', ({'phone_number': phone_number, 'password': password}, message)))
#         s.run()

def periodic(scheduler, interval, params, action, actionargs=()):
    if params['step'] <= params['stop']:
        scheduler.enter((interval *  params['step']), 1, periodic,
            (scheduler, interval, params, action, actionargs))
        action(*actionargs)
        params['step'] += 1
    scheduler.run()


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


@task(base=DBTask, name="facenew.task.task.assing_new_task", ignore_result=True)
def assing_new_task():
    crontabs = Message.objects.filter(type_message='facebook', enabled=True).values_list('crontab', flat=True).distinct('crontab')
    user_enabled = [[int(item2) for item2 in item] for item in [e.strip('[]').split(',') if e != '[]' else [0,0] for e in PeriodicTask.objects.exclude(enabled=False).values_list('args', flat=True).distinct('args')]]
    users = {}
    for userd in user_enabled:
        if sum(userd) > 0:
            if userd[0] not in users:
                users.update({userd[0]: []})
            if len(userd) > 1:
                users[userd[0]].append(userd[1])

    userso = User.objects.filter(pk__in=users.keys())
    crontabo = CrontabSchedule.objects.filter(pk__in=crontabs)

    for user in userso:
        m = list(set(crontabs) - set(users[user.id]))
        for n in m:
            for interval_crontab in crontabo:
                if interval_crontab.id == n:
                    task_name = slug("{0}-{1}".format(user.facebook_username, interval_crontab))
                    periodic_task = PeriodicTask(name=task_name, task='facenew.tasks.tasks.publish', crontab=interval_crontab, enabled=True, args=[user.id, interval_crontab.id])
                    periodic_task.save()
                    user_periodic_task = UserCrontabSchedule(user=user, periodic_task=periodic_task)
                    user_periodic_task.save()

