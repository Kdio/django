from django.db import models
from django.db.models.signals import pre_save
from django.utils.translation import gettext_lazy as _
from app.utils.validators import validate_non_zero

class Lancamento(models.Model):
    """ Lancamento class """
    rubrica = models.ForeignKey(
        'app.Rubrica', on_delete=models.CASCADE, verbose_name=_('Rúbrica'),
        related_name='lancamentos')
    historico = models.CharField(max_length=250, blank=True, verbose_name=_('Histórico'))
    data = models.DateField(verbose_name=_('Data'))
    valor = models.DecimalField(decimal_places=2, max_digits=15,
        validators=[validate_non_zero], verbose_name=_('Valor'))

    class Meta:
        ordering = ['-data', 'rubrica__nome','historico']
        verbose_name = _('Lançamento')
        verbose_name_plural = _('Lançamentos')

    def __str__(self):
        return f"{self.rubrica}/{self.historico}"

    def __repr__(self):
        return self.__str__()

    def can_delete(self):
        return True

    def tipo(self):
        """ Caixa tipo method """
        return self.rubrica.tipo

    def str_tipo(self):
        """ Caixa str_tipo method """
        return self.rubrica.str_tipo()

def verify_value_flag(sender, instance, **kwargs):
    """ Before save trigger """
    if instance.rubrica is None: return
    # If creating
    if instance.id is None:
        instance.valor *= instance.rubrica.tipo
    else:
        # If updating
        previous = Lancamento.objects.get(id=instance.id)
        if instance.rubrica.tipo == previous.rubrica.tipo: return
        instance.valor *= -1

""" Register before save trigger """
pre_save.connect(verify_value_flag, sender=Lancamento)
