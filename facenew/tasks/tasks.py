# -*- coding: utf-8 -*-

from celery import task
from facenew.tasks.models import Message
from fandjango.models import User
from facenew.whatsapp.models import Telephone
from facenew.whatsapp.models import Account
from unidecode import unidecode


import time, datetime
import threading,time, base64

from Yowsup.connectionmanager import YowsupConnectionManager
from Yowsup.Common.utilities import Utilities
from Yowsup.Common.debugger import Debugger
from Yowsup.Common.constants import Constants
from facenew.whatsapp.ValidClient import WhatsappValidClient

Debugger.enabled = False

import facebook


@task()
def publish(user_id, post_id):
    facebook_user = User.objects.get(pk=user_id)
    message = Message.objects.get(pk=int(post_id))
    if facebook_user and message:
        graph = facebook.GraphAPI(facebook_user.oauth_token.token)
        data = {
             "caption": message.caption.encode('utf-8'),
             "description": message.description.encode('utf-8'),
             "picture": 'http://colaboradores.nethub.co/' + message.image.url
        }
        return graph.put_wall_post(message.message.encode('utf-8'), data, "me")


@task()
def exists_whatsapp(account):
    phone = Telephone.objects.filter(busy=False, updated=False).first()
    print phone, "asi quedooo"
    if phone:
        phone.busy = True
        phone.save()
        print phone.phone
        account = Account.objects.get(phone=account)
        password = base64.b64decode(bytes(account.password.encode('utf-8')))
        phone_number = account.phone
        keepAlive = True
        wa = WhatsappValidClient(phone_number, keepAlive, True, phone.phone, phone)
        wa.login(phone_number, password)
    pass