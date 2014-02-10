
from celery import task
from publishing.tasks.models import Message
from social.apps.django_app.default.models import UserSocialAuth

import facebook

token = {"access_token": "CAADgCTcCCg4BAKStys6koN1aMcjp8n0MlprX3dl4mM0qhLtVDwH7OMWkZCzcJupN5Y6CTcz683lPLLW5X7jrQaPSWVJR95KnPkkMWqW3t2bnHQZCztP84LeAJZCpUuPYGwYd6XIbA7qVSWXmIBrt7cJjUs6ZCEo7JZBzU3118e5QCGBX1KFKe", "expires": "5171935", "id": "548048173"}
# try:
#     import pymongo
# except ImportError: # pragma: no cover
#     pymongo = None # noqa


# if pymongo:
#     try:
#         from bson.binary import Binary
#     except ImportError: # pragma: no cover
#         from pymongo.binary import Binary # noqa
# else: # pragma: no cover
#     Binary = None 


# class DebugTask(Task):
# 	abstract = True

# 	def after_return(self, status, retval, task_id, args, kwargs, einfo):
# 		pass
# 		# self.backend.collection.update({'_id': task_id}, {"$set": {'arguments': Binary(self.backend.encode(args))}})
# 		# obj = self.backend.collection.find_one({'_id': task_id})
# 		# print(self.backend.decode(obj['arguments']), self.backend.decode(obj['result']))


@task()
def publish(user_id, post_id):
    user = UserSocialAuth.objects.get(user_id=user_id)
    message = Message.objects.get(pk=int(post_id))
    if user and message:
        graph = facebook.GraphAPI(user.extra_data['access_token'])
        data = {
             "caption": message.caption.encode('ascii', 'ignore'),
             "description": message.description.encode('utf-8').strip(),
             "picture": 'http://localhost/' + message.image.url
        }
        return graph.put_wall_post(message.message, data, "me")