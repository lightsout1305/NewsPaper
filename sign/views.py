from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView
from .forms import BaseRegisterForm, ProfileUpdateForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from news_project.models import Author


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'profile_update.html'
    model = User
    form_class = ProfileUpdateForm
    success_url = '/'

    def get_object(self, **kwargs):
        return self.request.user


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
        Author.objects.create(author_user_id=user.id)
    return redirect('/main/')


@login_required
def degrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if request.user.groups.filter(name='authors').exists():
        authors_group.user_set.remove(user)
        Author.objects.get(author_user_id=user.id).delete()
    return redirect('/main/')
