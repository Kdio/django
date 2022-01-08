from django.db import models
from django.utils.translation import gettext_lazy as _

DEBITO = -1
CREDITO = 1

TIPO_RUBRICA = [(DEBITO, _('Débito')), (CREDITO, _('Crédito'))]

class Rubrica(models.Model):
    """ Rubrica class """
    nome = models.CharField(max_length=50, unique=True, null=False, verbose_name=_('Nome'))
    tipo = models.IntegerField(default=1, null=False, choices=TIPO_RUBRICA, verbose_name=_('Tipo'))

    class Meta:
        ordering = ['nome']
        verbose_name = _('Rúbrica')
        verbose_name_plural = _('Rúbricas')

    def __str__(self):
        return self.nome

    def __repr__(self):
        return self.__str__()

    def can_delete(self):
        return len(self.lancamentos.all()) == 0

    def str_tipo(self):
        """ Rubrica str_tipo method """
        return _('Crédito') if self.tipo == 1 else _('Débito')

    @classmethod
    def choices(class_, include_all=False):
        """ Rubrica choices method """
        choices = [(r.id, r.nome) for r in class_.objects.all()]
        if include_all: choices.insert(0, ("all", "(Todas)"))
        return choices
