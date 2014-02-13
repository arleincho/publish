from __future__ import unicode_literals

from django.db import models


class Telephone(models.Model):

    phone = models.CharField('Numero de Telefono', max_length=12, blank=False, null= False, unique=True)
    base = models.CharField('Base de datos Origen', max_length=50, blank=False)
    exists = models.BooleanField('Existe en Whatsapp', default=False, blank=False)
    last_seen = models.DateTimeField('Ultima vez visto', null=True, default=None)
    busy = models.BooleanField('Esta siendo verificado', default=False, blank=False)
    updated = models.BooleanField('Ya fue verificado', default=False, blank=False)
    checked_at = models.DateTimeField('Fecha de la Consulta', auto_now=True, null=True, default=None)
    
    def __str__(self):
        return "{0}-{1}".format(self.base, self.phone)


class Account(models.Model):

    cc = models.CharField('Codigo del Pais', max_length=4, blank=False, null=False, default="57")
    phone = models.CharField('# Telefono con CC', max_length=50, blank=False)
    identifier = models.CharField('Identificador IMEI o MAC', max_length=50, blank=True, null=True)
    password = models.CharField('Password de la cuenta', max_length=30, null=False)
    enabled = models.BooleanField('Habilitada', default=True)
    
    def __str__(self):
        return "{0}".format(self.phone)


class MessagesTelephone(models.Model):

    phone = models.ForeignKey(
        Telephone, null=False, blank=False, help_text=('Telefono al que se le envia'),
    )
    message = models.ForeignKey(
        Message, null=False, blank=False, help_text=('Mensaje a Enviar'), limit_choices_to={'type_message': 'watsapp'}
    )