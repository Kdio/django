from datetime import date
from django.db import models
from django.db.models.signals import pre_save
from django.utils.translation import gettext_lazy as _

class Contratacao(models.Model):
    """ Contratacao class """
    contrato = models.ForeignKey(
        'app.Contrato', null=False, on_delete=models.CASCADE, verbose_name=_('Contrato'),
        related_name='contratacoes')
    associado = models.ForeignKey(
        'app.Associado', null=False, on_delete=models.CASCADE, verbose_name=_('Associado'),
        related_name='contratacoes')
    descricao = models.CharField(max_length=250, blank=True, verbose_name=_('Descrição'))
    valor = models.DecimalField(
        decimal_places=2, max_digits=15, null=False, verbose_name=_('Valor'))
    ativa = models.BooleanField(default=True, null=False, verbose_name=_('Ativa'))
    historico = models.TextField(blank=True, verbose_name=_('Histórico'))

    class Meta:
        ordering = ['associado__nome', '-ativa', 'contrato__nome', 'descricao']
        verbose_name = _('Contratação')
        verbose_name_plural = _('Contratações')

    def __str__(self):
        return f"{self.associado}/{self.contrato}/{self.descricao}"

    def __repr__(self):
        return self.__str__()

    def can_delete(self):
        return len(self.alineas.all()) == 0

    @classmethod
    def ativas(class_):
        """ Contratacao ativas method """
        return class_.objects.filter(ativa=True)

    @classmethod
    def associados_ativos(class_):
        """ Contratacao associados_ativos method """
        return sorted(list(set(class_.ativas().values_list("associado_id", flat=True))))

    @classmethod
    def ativas_do_associado(class_, associado_id):
        """ Contratacao ativas_do_associado method """
        return class_.ativas().filter(associado_id=associado_id)


def initialize_historico_on_create(sender, instance, **kwargs):
    """ Before create trigger """
    if instance.id is None:
        instance.historico=f"Adicionada em {date.today().strftime('%d/%m/%Y')}"

""" Register before save trigger """
pre_save.connect(initialize_historico_on_create, sender=Contratacao)
