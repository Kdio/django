from django.contrib.auth.forms import AuthenticationForm, UsernameField, PasswordChangeForm
from django.forms import TextInput, CharField, PasswordInput
from django.utils.translation import gettext_lazy as _


class LogInForm(AuthenticationForm):
    username = UsernameField(
        label=_("Nome"),
        widget=TextInput(
            attrs={
                'autofocus': True,
                'class': 'input',
                'id': 'djl-el-login-form-username-field'
            }))
    password = CharField(
        label=_("Senha"),
        strip=False,
        widget=PasswordInput(
            attrs={
                'autocomplete': 'current-password',
                'class': 'input',
                'id': 'djl-el-login-form-password-field'
            }),
    )


class MyPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].widget = PasswordInput(attrs={"class": "form-control"})
        self.fields["new_password1"].widget = PasswordInput(attrs={"class": "form-control"})
        self.fields["new_password2"].widget = PasswordInput(attrs={"class": "form-control"})
