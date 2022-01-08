from datetime import date
from django import template
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static
from app.utils.public import date_to_str
from app.models.competencia import Competencia

register = template.Library()

@register.simple_tag(name='setvar')
def setvar(value=None):
  return value

@register.filter(name='static_file')
def static_file(file):
    with open(f"{settings_value('BASE_DIR')}/{settings_value('STATIC_URL')}{file}","r") as f:
      string = f.read()
    return string

@register.filter(name='get_item_by_index')
def get_item_by_index(indexable, i):
    return indexable[i]

@register.filter(name='default_alert_icon')
def default_alert_icon(icon):
    if icon == "success": icon = "far fa-check-circle"
    if icon == "warning": icon = "fas fa-exclamation-triangle"
    if icon == "danger" or icon == "error": icon = "fas fa-radiation"
    return icon

@register.filter(name='default_submit_caption')
def default_submit_caption(caption):
    return caption or _("Salvar")

@register.filter(name='default_search_caption')
def default_search_caption(caption):
    return caption or _("Pesquisar")

@register.filter(name='default_back_caption')
def default_back_caption(caption):
    return caption or _("Voltar")

@register.filter(name='default_back_url')
def default_back_url(url):
    return url or reverse('home')

@register.filter(name='settings_value')
def settings_value(name):
    return getattr(settings, name, "")

@register.simple_tag(name='current_competencia')
def current_competencia():
    return Competencia.current()

@register.filter(name='show_item')
def show_item(instance, field):
    value = getattr(instance, field)
    if not value: return ''
    if isinstance(value, date): value = date_to_str(value)
    caption = type(instance)._meta.get_field(field).verbose_name
    return f'<div class="mb-2 show-item">{caption}: <strong>{value}</strong></div>'


CSS_CLASSES = {
  '': "",
  'a': "table-actions d-print-none",
  'c': "text-center",
  'r': "text-right",
}

@register.filter(name='css_class')
def css_class(i):
    return CSS_CLASSES[i]


