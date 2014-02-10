from django import forms
from djcelery.models import IntervalSchedule
from djcelery.models import CrontabSchedule
from publishing.tasks.models import Message

from django.utils.translation import ugettext as _

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
