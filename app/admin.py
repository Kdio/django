from django.contrib import admin

# Register your models here.

from app.models.usuario import Usuario
from app.models.rubrica import Rubrica
from app.models.lancamento import Lancamento
from app.models.contrato import Contrato
from app.models.associado import Associado
from app.models.contratacao import Contratacao

admin.site.register(Usuario)
admin.site.register(Rubrica)
admin.site.register(Lancamento)
admin.site.register(Contrato)
admin.site.register(Associado)
admin.site.register(Contratacao)
