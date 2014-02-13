# -*- coding: utf-8 -*-

from django import forms
from djcelery.models import IntervalSchedule
from djcelery.models import CrontabSchedule
from facenew.tasks.models import Message

from django.utils.translation import ugettext as _

TIME_INTERVALS = [
    {"text": "Dos Mensajes Diarios", "interval_id": 1, 'type': 'interval', 'id': 1},
    {"text": "Un Mensaje Diario", "interval_id": 1, 'type': 'interval', 'id': 2},
    {"text": "Cuatro Mensajes a La Semana", "interval_id": 1, 'type': 'interval', 'id': 3},
    {"text": "Tres Mensajes a La Semana", "interval_id": 1, 'type': 'interval', 'id': 4},
    {"text": "Dos Mensajes a La Semana", "interval_id": 1, 'type': 'interval', 'id': 5},
    {"text": "Uno Mensaje a La Semana", "interval_id": 1, 'type': 'interval', 'id': 6},
    {"text": u"Uno Solo Mensaje (solo Un Día)".encode('utf-8'), "interval_id": 1, 'type': 'interval', 'id': 7},
]

class PublishingForm(forms.Form):

    def __init__(self, *args, **kwargs):
       super(PublishingForm, self).__init__(*args, **kwargs)
       self.fields['interval'].choices = self.get_intervals()
       self.fields['message'].choices = self.get_messages()
       self.fields['cron'].choices = self.get_crons()

    def get_intervals(self):
        entries = IntervalSchedule.objects.all()
        INTERVALS = [(interv.id, 'cada {0}'.format(_(interv.period)[:-1]) if interv.every == 1 else 'cada {0} {1}'.format(interv.every, _(interv.period))) for interv in entries]
        INTERVALS.insert(0, ('', '----'))
        return INTERVALS

    def get_crons(self):
        crons = CrontabSchedule.objects.filter()
        CRONS = [(cron.id, "A las {0.hour} horas".format(cron) if cron.minute == "*" else "A las {0.hour} horas y {0.minute} minutos".format(cron)) for cron in crons]
        CRONS.insert(0, ('', '----'))
        return CRONS

    def get_messages(self):
        messages = Message.objects.filter(enabled=True)
        MESSAGES = [(message.id, message.caption) for message in messages]
        MESSAGES.insert(0, ('', '----'))
        return MESSAGES

    TYPE_INTERVAL = [('interval', 'Intervalo de Tiempo'),('cron', 'Momento Especifico')]

    type_interval = forms.ChoiceField(choices=TYPE_INTERVAL, widget=forms.RadioSelect())

    interval = forms.ChoiceField(
        required=False,
        label='Intervalo de Tiempo'
    )

    cron = forms.ChoiceField(
        required=False,
        label='Momento Especifico'
    )

    message = forms.ChoiceField(
        required=True,
        label='Mensaje a Publicar'
    )

class SelectOptionForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(SelectOptionForm, self).__init__(*args, **kwargs)
        self.fields['interval'].choices = [(interval['id'], interval['text']) for interval in TIME_INTERVALS]

    interval = forms.ChoiceField(
        required=True,
        label='Intervalo de Tiempo'
    )













