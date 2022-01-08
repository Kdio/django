import decimal
from datetime import date
from dateutil import relativedelta
from django.db import models
from django.db.models.signals import pre_save
from django.utils.translation import gettext_lazy as _
from app.utils.validators import validate_non_zero


class Mensalidade(models.Model):
    """ Mensalidade class """
    associado = models.ForeignKey(
        'app.Associado', on_delete=models.CASCADE, verbose_name=_('Associado'),
        related_name='mensalidades')
    competencia = models.ForeignKey(
        'app.Competencia', on_delete=models.CASCADE, verbose_name=_('Competência'),
        related_name='mensalidades')
    data_vence = models.DateField(verbose_name=_('Data de Vecimento'))
    multa = models.DecimalField(
        decimal_places=2, max_digits=15, blank=True, null=True, verbose_name=_('Multa'))
    saldo = models.DecimalField(
        decimal_places=2, max_digits=15, blank=True, null=True, verbose_name=_('Saldo'))
    data_pgto = models.DateField(blank=True, null=True, verbose_name=_('Data de Pagamento'))
    valor_pgto = models.DecimalField(
        decimal_places=2, max_digits=15, blank=True, null=True,
        verbose_name=_('Valor do Pagamento'))

    PERCENTUAL_JUROS_MES = 0.01
    PERCENTUAL_MULTA = 0.10

    class Meta:
        unique_together = (('associado', 'competencia'))
        ordering = ['associado__nome', '-competencia__ano', '-competencia__mes']
        verbose_name = _('Mensalidade')
        verbose_name_plural = _('Mensalidades')


    def __str__(self):
        return f"{self.competencia}/{self.associado}/{self.data_vence}"


    def __repr__(self):
        return self.__str__()


    def can_delete(self):
        return False


    def valor(self):
        """ Mensalidade valor method """
        soma = 0
        for alinea in self.alineas.all(): soma += alinea.valor
        return soma


    def juros(self):
        """ Mensalidade juros method """
        # Se ainda não venceu ou pagou em dia
        if self.data_vence >= date.today() or \
            (self.data_pgto and self.data_vence >= self.data_pgto): return 0
        if self.data_pgto:
            data_end = self.data_pgto
        else:
            data_end = date.today()
        diff = relativedelta.relativedelta(data_end, self.data_vence)
        months = diff.months + (12 * diff.years)
        # Se ainda não passou 1 mês
        if months == 0: return 0
        soma = self.valor()
        for _x in range(months):
            soma += soma * decimal.Decimal(self.PERCENTUAL_JUROS_MES)
        return round(soma - self.valor(), 2)


    def total(self):
        """ Mensalidade total method """
        soma = self.valor()
        if self.multa: soma += self.multa
        if self.saldo: soma -= self.saldo
        soma += self.juros()
        return soma


def verify_saldo_anterior(sender, instance, **kwargs):
    """ Before save trigger """
    if instance.id is None and instance.associado_id:
        last = Mensalidade.objects.filter(
            associado_id=instance.associado_id).order_by('-id').first()
        if last and last.valor_pgto:
            instance.saldo = last.valor_pgto - last.total()

""" Register before save trigger """
pre_save.connect(verify_saldo_anterior, sender=Mensalidade)
