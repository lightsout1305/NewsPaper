from django.contrib.auth.forms import UserCreationForm
from allauth.account.forms import SignupForm
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext as _
from django import forms


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email')
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')

    class Meta:
        model = User
        fields = ('username',
                  'first_name',
                  'last_name',
                  'email',
                  'password1',
                  'password2',
                  )
        labels = {'username': 'Псевдоним', 'first_name': 'Имя', 'last_name': 'Фамилия',
                  'email': 'Электронная почта', 'password1': 'Придумайте пароль',
                  'password2': 'Подтвердите пароль'}


class CommonSignupForm(SignupForm):

    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user


class ProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = _("Username")
        self.fields["first_name"].label = _("First name")
        self.fields["last_name"].label = _("Last name")
        self.fields["email"].label = _("E-mail")

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email'
        ]
