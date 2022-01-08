from django.db import models
from django.utils.translation import gettext_lazy as _

class Contrato(models.Model):
    """ Contrato class """
    nome = models.CharField(max_length=50, unique=True, null=False, verbose_name=_('Nome'))

    class Meta:
        ordering = ['nome']
        verbose_name = _('Contrato')
        verbose_name_plural = _('Contratos')

    def __str__(self):
        return self.nome

    def __repr__(self):
        return self.__str__()

    def can_delete(self):
        return len(self.contratacoes.all()) == 0

    @classmethod
    def choices(class_, include_all=False):
        """ Rubrica choices method """
        choices = [(r.id, r.nome) for r in class_.objects.all()]
        if include_all: choices.insert(0, ("all", "(Todos)"))
        return choices
