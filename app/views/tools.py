import os
import shutil
import markdown
import markdown.extensions.fenced_code
import markdown.extensions.sane_lists
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from app.forms.upload import UploadForm

@login_required
def backup(request):
    if request.method == 'POST':
        with open(settings.DATABASE_FILE, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/octet-stream")
            content = f'inline; filename={os.path.basename(settings.DATABASE_FILE)}'
            response['Content-Disposition'] = content
            return response
    context = { 'title':_("Salvar dados") }
    return render(request, 'tools/backup.html', context)


@staff_member_required
def restore(request):
    uploaded = ""
    form = UploadForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        temp = os.path.join(settings.MEDIA_ROOT, 'temp_db')
        default_storage.save(temp, ContentFile(request.FILES['file'].read()))
        shutil.copy(temp, settings.TEST_DATABASE_FILE)
        os.remove(temp)
        messages.success(request, _("Banco de dados restaurado com sucesso"))
        return redirect('home')
    context = { 'title':_("Restaurar dados"), 'form': form}
    return render(request, 'tools/restore.html', context)


@login_required
def model(request):
    context = { 'title':_("Modelo de dados") }
    return render(request, 'tools/model.html', context)


@login_required
def help(request):
    root_path = getattr(settings, 'BASE_DIR', "")
    file = open(f"{root_path}/README.markdown", mode="r", encoding="utf-8")
    help_text = markdown.markdown(file.read().split(
        "# Technical specifications")[0], extensions=["fenced_code", 'sane_lists'])
    file.close()

    file = open(f"{root_path}/CHANGELOG", mode="r", encoding="utf-8")
    changelog = process_changelog(file.read())
    file.close()

    context = { 'title':_("Ajuda do sistema"), 'text':f"{help_text}<br />{changelog}"}
    return render(request, 'tools/help.html', context)


def process_changelog(text):
    """ process_changelog method """
    versions = text.split("## [")
    versions.pop(0)
    changelog = ""
    for version in versions:
        itens = []
        chapters = version.split("### ")
        changelog += f"<strong>{_('Versão')} {chapters.pop(0).replace(']', '')}</strong><br /><ul>"
        for chapter in chapters:
            itens = chapter.split("- ")
            changelog += f"<li>{itens.pop(0)}</li><ul>"
            for item in itens:
                changelog += f"<li>{item}</li>"
            changelog += "</ul>"
        changelog += "</ul>"
    changelog = f"<h4>Controle de versões</h4><details><summary>({_('Clique para visualizar')})</summary>{changelog}</details>"
    return changelog
