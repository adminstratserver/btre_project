from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import MemberProfile


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = MemberProfile
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = MemberProfile
        fields = ('email',)