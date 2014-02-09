from django import forms
from djcelery.models import IntervalSchedule

class PublishingForm(forms.Form):

    def __init__(self, *args, **kwargs):
       super(PublishingForm, self).__init__(*args, **kwargs)
       self.fields['interval'].choices = self.get_intervals()

    def get_intervals(self):
        entries = IntervalSchedule.objects.all()
        INTERVALS = [(interv.id, 'every {0.period_singular}'.format(interv) if interv.every == 1 else 'every {0.every} {0.period}'.format(interv)) for interv in entries]
        INTERVALS.insert(0, ('', '----'))
        return INTERVALS
    
    interval = forms.ChoiceField(
        required=True,
        label='Intervalo de Tiempo')

    def clean_message(self):
        message = self.cleaned_data['interval']
        raise forms.ValidationError("Not enough words!")
