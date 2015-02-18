'''
Copyright (c) <2012> Tarek Galal <tare2.galal@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this 
software and associated documentation files (the "Software"), to deal in the Software 
without restriction, including without limitation the rights to use, copy, modify, 
merge, publish, distribute, sublicense, and/or sell copies of the Software, and to 
permit persons to whom the Software is furnished to do so, subject to the following 
conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR 
A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
from Yowsup.connectionmanager import YowsupConnectionManager

import time, datetime, sys

if sys.version_info >= (3, 0):
    raw_input = input


class WhatsappValidClient:
    
    def __init__(self, phoneNumber, keepAlive = False, sendReceipts = False, toValidate="", object_phone=None):
        self.sendReceipts = sendReceipts
        self.phoneNumber = phoneNumber
        self.jid = "%s@s.whatsapp.net" % phoneNumber
        self.toValidate = toValidate
        self.object_phone = object_phone
        
        self.sentCache = {}
        
        connectionManager = YowsupConnectionManager()
        connectionManager.setAutoPong(keepAlive)
        self.signalsInterface = connectionManager.getSignalsInterface()
        self.methodsInterface = connectionManager.getMethodsInterface()
        
        self.signalsInterface.registerListener("auth_success", self.onAuthSuccess)
        self.signalsInterface.registerListener("auth_fail", self.onAuthFailed)
        self.signalsInterface.registerListener("presence_updated", self.onPresenceUpdated)
        self.signalsInterface.registerListener("exists", self.onExists)
        
        self.done = False
        self.not_send = False
    
    def login(self, username, password):
        self.username = username
        self.methodsInterface.call("auth_login", (username, password))

        while not self.done:
            time.sleep(0.5)

    def onExists(self, jid, exists):
        if not exists:
            self.object_phone.exists = False
            self.object_phone.busy = False
            self.object_phone.updated = True
            self.object_phone.save()
            print "no existe {0}".format(jid)
        self.done = True
        

    def onPresenceUpdated(self, jid, lastSeen):
        formattedDate = datetime.datetime.fromtimestamp(long(time.time()) - lastSeen).strftime('%Y-%m-%d %H:%M')
        self.object_phone.exists = True
        self.object_phone.busy = False
        self.object_phone.updated = True
        self.object_phone.last_seen = formattedDate
        self.object_phone.save()
        print "existe {0}".format(jid)
        self.done = True

    def onAuthSuccess(self, username):
        self.methodsInterface.call("presence_request", ("%s@s.whatsapp.net" % self.toValidate,))
        self.methodsInterface.call("ready")

    def onAuthFailed(self, username, err):
        print("Auth Failed! %s" % err)
        self.done = True

