import datetime
import decimal
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from app.models.contratacao import Contratacao
from app.models.mensalidade import Mensalidade
from app.models.alinea import Alinea


MESES = [
    ('01', _('Janeiro')), ('02', _('Fevereiro')), ('03', _('Março')), ('04', _('Abril')),
    ('05', _('Maio')), ('06', _('Junho')), ('07', _('Julho')), ('08', _('Agosto')),
    ('09', _('Setembro')), ('10', _('Outubro')), ('11', _('Novembro')), ('12', _('Dezembro'))
]


class Competencia(models.Model):
    """ Competencia class """
    ano = models.CharField(max_length=4, unique=False, null=False, verbose_name=_('Ano'))
    mes = models.CharField(
        max_length=2, unique=False, null=False, choices=MESES, verbose_name=_('Mês'))
    data = models.DateField(blank=False, null=False, verbose_name=_('Data'))

    DEFAULT_DAY = 25

    class Meta:
        unique_together = (('ano', 'mes'))
        ordering = ['-ano', '-mes']
        verbose_name = _('Competência')
        verbose_name_plural = _('Competências')

    def __str__(self):
        return f"{self.ano}/{self.mes}"

    def __repr__(self):
        return self.__str__()

    def can_delete(self):
        return False

    @classmethod
    def current(class_):
        """ Competencia current method """
        return class_.objects.first()

    @classmethod
    def proxima(class_):
        """ Competencia proxima method """
        current = class_.current()
        ano = int(current.ano)
        mes = int(current.mes) + 1
        if mes == 13:
            ano += 1
            mes = 1
        return class_(
            ano=str(ano), mes=str(mes).zfill(2),
            data=datetime.datetime(ano, mes, class_.DEFAULT_DAY))


    @classmethod
    @transaction.atomic
    def create(class_):
        # Atribui multas onde necessário
        multas = Mensalidade.objects.filter(data_pgto__isnull=True).all()
        for mensalidade in multas:
            mensalidade.multa = mensalidade.valor() * decimal.Decimal(Mensalidade.PERCENTUAL_MULTA)
            mensalidade.save()

        """ Competencia create method """
        # Abre nova competência
        competencia = class_.proxima()
        competencia.save()
        for associado_id in Contratacao.associados_ativos():
            mensalidade = Mensalidade.objects.create(
                competencia_id=competencia.id, associado_id=associado_id,
                data_vence=competencia.data)
            for contratacao in Contratacao.ativas_do_associado(associado_id):
                Alinea.objects.create(
                    mensalidade_id=mensalidade.id, contratacao_id=contratacao.id,
                    valor=contratacao.valor)
