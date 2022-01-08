from django.db import models
from django.utils.translation import gettext_lazy as _

class Associado(models.Model):
    """ Associado class """
    nome = models.CharField(max_length=50, null=False, verbose_name=_('Nome'))
    matricula = models.CharField(
        max_length=20, unique=True, blank=True, null=True, verbose_name=_('Matrícula'))
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Telefone'))

    class Meta:
        ordering = ['nome']
        verbose_name = _('Associado')
        verbose_name_plural = _('Associados')

    def __str__(self):
        return self.nome

    def __repr__(self):
        return self.__str__()

    def can_delete(self):
        return len(self.contratacoes.all()) == 0
