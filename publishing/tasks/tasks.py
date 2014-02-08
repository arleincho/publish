from celery import task
from celery import Task

import facebook

token = {"access_token": "CAADgCTcCCg4BAKStys6koN1aMcjp8n0MlprX3dl4mM0qhLtVDwH7OMWkZCzcJupN5Y6CTcz683lPLLW5X7jrQaPSWVJR95KnPkkMWqW3t2bnHQZCztP84LeAJZCpUuPYGwYd6XIbA7qVSWXmIBrt7cJjUs6ZCEo7JZBzU3118e5QCGBX1KFKe", "expires": "5171935", "id": "548048173"}
try:
    import pymongo
except ImportError: # pragma: no cover
    pymongo = None # noqa


if pymongo:
    try:
        from bson.binary import Binary
    except ImportError: # pragma: no cover
        from pymongo.binary import Binary # noqa
else: # pragma: no cover
    Binary = None 


class DebugTask(Task):
	abstract = True

	def after_return(self, status, retval, task_id, args, kwargs, einfo):
		pass
		# self.backend.collection.update({'_id': task_id}, {"$set": {'arguments': Binary(self.backend.encode(args))}})
		# obj = self.backend.collection.find_one({'_id': task_id})
		# print(self.backend.decode(obj['arguments']), self.backend.decode(obj['result']))




@task(base=DebugTask)
def publish(message=None):
    graph = facebook.GraphAPI(token['access_token'])
    return graph.put_object("me", "feed", message="task...!")