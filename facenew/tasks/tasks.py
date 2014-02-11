# -*- coding: utf-8 -*-

from celery import task
from facenew.tasks.models import Message
from fandjango.models import User
from unidecode import unidecode

import facebook


@task()
def publish(user_id, post_id):
    facebook_user = User.objects.get(pk=user_id)
    message = Message.objects.get(pk=int(post_id))
    if facebook_user and message:
        graph = facebook.GraphAPI(facebook_user.oauth_token.token)
        print message.caption.encode('ascii', 'xmlcharrefreplace')
        data = {
             "caption": message.caption.encode('utf-8'),
             "description": message.description.encode('utf-8'),
             "picture": 'http://localhost/' + message.image.url
        }
        return graph.put_wall_post(message.message.encode('utf-8'), data, "me")