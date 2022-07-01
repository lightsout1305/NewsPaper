from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView
from .forms import BaseRegisterForm, ProfileUpdateForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'profile_update.html'
    model = User
    form_class = ProfileUpdateForm
    success_url = '/main/'

    def get_object(self, **kwargs):
        return self.request.user


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/main/')


# Create your views here.
