from allauth.socialaccount.forms import SignupForm
from django.contrib.auth.models import Group


class MyCustomSocialSignupForm(SignupForm):

    def save(self, request):
        user = super(MyCustomSocialSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user
