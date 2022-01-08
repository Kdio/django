from django.db import models
from django.utils.translation import gettext_lazy as _

class Alinea(models.Model):
    """ Alinea class """
    mensalidade = models.ForeignKey(
        'app.Mensalidade', on_delete=models.CASCADE, verbose_name=_('Mensalidade'),
        related_name='alineas')
    contratacao = models.ForeignKey(
        'app.Contratacao', on_delete=models.CASCADE, verbose_name=_('Contratacao'),
        related_name='alineas')
    valor = models.DecimalField(decimal_places=2, max_digits=15, verbose_name=_('Valor'))

    class Meta:
        unique_together = (('mensalidade', 'contratacao'))
        ordering = ['contratacao__contrato__nome']
        verbose_name = _('Alínea')
        verbose_name_plural = _('Alíneas')

    def __str__(self):
        return f"{self.mensalidade}/{self.contratacao}"

    def __repr__(self):
        return self.__str__()

    def can_delete(self):
        return False
