# -*- coding: utf-8 -*-

from celery import task
from celery import Task
from celery.task import periodic_task
from django.conf import settings
from django.db import transaction
from facenew.whatsapp.models import Telephone
from facenew.whatsapp.models import Account
from facenew.whatsapp.models import MessagesPhoneWhatsapp


import base64
import datetime
import subprocess



class DBTask(Task):
    abstract = True



@task(base=DBTask, ignore_result=True)
def exists_whatsapp(account):
    try:
        phone = Telephone.objects.filter(busy=False, updated=False).first()
        if phone:
            phone.busy = True
            phone.save()
            account = Account.objects.get(phone=account)
            password = base64.b64decode(bytes(account.password.encode('utf-8')))
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

        script = settings.ROOT_PATH + "/whatsapp/lib/whatsapp/send.php"

        print "/usr/bin/php5 {0} {1} '{2}' {3} {4} '{5}' {6}".format(
            script, phone_number, '', password, phone.phone, message.message.encode('utf-8'), message_phone_whatsapp.id)

        subprocess.call(["/usr/bin/php5 {0} {1} '{2}' {3} {4} '{5}' {6} '{7}'".format(
            script, phone_number, '', password, phone.phone, message.message.encode('utf-8'), message_phone_whatsapp.id)
        ], shell=True)
    except Exception, e:
        transaction.rollback()
        print str(e)

