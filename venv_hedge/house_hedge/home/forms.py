from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Member

class MemberCreationForm(UserCreationForm):
    class Meta:
        model = Member
        fields = ("email",)

class MemberChangeForm(UserChangeForm):
    class Meta:
        model = Member
        fields = ("email",)